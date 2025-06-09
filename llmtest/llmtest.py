import asyncio
import aiohttp
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import json
import argparse
import threading
from queue import Queue
import asyncio.subprocess

class LLMResponseHandler:
    def __init__(self, result_dir: Path, summary_file: Path):
        self.result_dir = result_dir
        self.summary_file = summary_file
        self.response_queues = {}
        self.handlers = {}
        self.success_count = 0
        self.total_count = 0
        self.total_time = 0
        self.total_elapsed_time = 0
        self.summary_written = False
        self.last_token_times = {}  # test_case_num -> last_token_time
        self.token_counts = {}  # test_case_num -> token_count
        self.first_token_times = {}  # test_case_num -> first_token_time
        self.start_times = {}  # test_case_num -> start_time
        
    def start_handling(self, test_case_num: int, start_time: float):
        queue = Queue()
        self.response_queues[test_case_num] = queue
        self.total_count += 1
        self.last_token_times[test_case_num] = start_time
        self.token_counts[test_case_num] = 0
        self.first_token_times[test_case_num] = None
        self.start_times[test_case_num] = start_time
        
        def handle_response():
            response_file = self.result_dir / f"tc{test_case_num:03d}.res"
            first_response = True
            full_response = []
            
            while True:
                response = queue.get()
                if response is None:  # 종료 신호
                    break

                # 첫 토큰까지의 시간 (Time To First Token, TTFT) Logging    
                if first_response:
                    elapsed_time = (time.time() - start_time) * 1000
                    start_time_str = datetime.fromtimestamp(start_time).strftime('%H%M%S.%f')[:-4]  # HHMMSS.xx 형식
                    with open(self.summary_file, "a", encoding="utf-8") as f:
                        f.write(f"tc{test_case_num:03d}.req,200,{start_time_str},{elapsed_time:.2f}\n")
                    self.success_count += 1
                    self.total_time += elapsed_time
                    first_response = False
                    self.first_token_times[test_case_num] = time.time()
                
                if isinstance(response, dict) and "response" in response:
                    full_response.append(response["response"])
                    self.last_token_times[test_case_num] = time.time()
                    self.token_counts[test_case_num] += 1
            
            # 전체 응답 저장
            with open(response_file, "w", encoding="utf-8") as f:
                f.write("".join(full_response))
            
            # 모든 처리가 끝나면 통계 정보 추가 (한 번만)
            if self.total_count == self.success_count and not self.summary_written:
                avg_time = self.total_time / self.success_count if self.success_count > 0 else 0
                avg_elapsed_time = self.total_elapsed_time / self.success_count if self.success_count > 0 else 0
                with open(self.summary_file, "a", encoding="utf-8") as f:
                    f.write(f"\n정상건수/전체건수: {self.success_count}/{self.total_count}\n")
                    f.write(f"평균 TTFT: {avg_time:.2f}ms\n")
                    f.write(f"평균 Elapsed Time: {avg_elapsed_time:.2f}ms\n")
                self.summary_written = True
        
        handler = threading.Thread(target=handle_response)
        handler.start()
        self.handlers[test_case_num] = handler
        
    def add_response(self, test_case_num: int, response: dict):
        if test_case_num in self.response_queues:
            self.response_queues[test_case_num].put(response)
            
    def finish_handling(self, test_case_num: int):
        if test_case_num in self.response_queues:
            self.response_queues[test_case_num].put(None)
            self.handlers[test_case_num].join()
            
            # 마지막 토큰까지의 총 시간 계산
            if test_case_num in self.last_token_times:
                elapsed_time = (self.last_token_times[test_case_num] - self.handlers[test_case_num]._start_time) * 1000
                self.total_elapsed_time += elapsed_time
                
                # TBT 계산
                tbt = 0
                if test_case_num in self.first_token_times and self.token_counts[test_case_num] > 1:
                    tbt = (self.last_token_times[test_case_num] - self.first_token_times[test_case_num]) * 1000 / (self.token_counts[test_case_num] - 1)
                
                # 기존 TTFT 라인에 Elapsed Time, Total Res Tokens, Avg TBT 추가
                with open(self.summary_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                with open(self.summary_file, "w", encoding="utf-8") as f:
                    for line in lines:
                        if line.startswith(f"tc{test_case_num:03d}.req"):
                            f.write(f"tc{test_case_num:03d}.req,200,{line.split(',')[2].strip()},{line.split(',')[3].strip()},{elapsed_time:.2f},{self.token_counts[test_case_num]},{tbt:.2f}\n")
                        else:
                            f.write(line)
            
            del self.response_queues[test_case_num]
            del self.handlers[test_case_num]
            if test_case_num in self.last_token_times:
                del self.last_token_times[test_case_num]
            if test_case_num in self.token_counts:
                del self.token_counts[test_case_num]
            if test_case_num in self.first_token_times:
                del self.first_token_times[test_case_num]
            if test_case_num in self.start_times:
                del self.start_times[test_case_num]

class LLMTester:
    def __init__(self, concurrent_users: int, test_cases: int):
        self.concurrent_users = concurrent_users
        self.test_cases = test_cases
        self.base_url = "http://localhost:11434/api/generate"
        self.request_dir = Path("request")
        self.response_dir = Path("response")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.result_dir = self.response_dir / self.timestamp
        self.summary_file = self.result_dir / "summary.txt"
        self.response_handler = LLMResponseHandler(self.result_dir, self.summary_file)
        
    async def setup(self):
        self.result_dir.mkdir(parents=True, exist_ok=True)
        with open(self.summary_file, "w", encoding="utf-8") as f:
            f.write("Test Case,Response Code,Start Time,TTFT (ms),Elapsed Time (ms),Total Res Tokens,Avg TBT (ms)\n")
    
    async def process_test_case(self, test_case_num: int):
        test_case_file = f"tc{test_case_num:03d}.req"
        test_case_path = self.request_dir / test_case_file
        
        if not test_case_path.exists():
            print(f"Warning: Test case file {test_case_file} not found")
            return
        
        with open(test_case_path, "r", encoding="utf-8") as f:
            request_data = f.read()
        
        start_time = time.time()
        self.response_handler.start_handling(test_case_num, start_time)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    json={
                        "model": "qwen2.5:7b",
                        "prompt": request_data,
                        "stream": True
                    }
                ) as response:
                    async for line in response.content:
                        if line:
                            try:
                                response_data = json.loads(line)
                                self.response_handler.add_response(test_case_num, response_data)
                            except json.JSONDecodeError:
                                continue
                            
            self.response_handler.finish_handling(test_case_num)
            print(f"Processed {test_case_file}")
            
        except Exception as e:
            print(f"Error processing {test_case_file}: {str(e)}")
            with open(self.summary_file, "a", encoding="utf-8") as f:
                f.write(f"{test_case_file},ERROR,{str(e)}\n")
            self.response_handler.finish_handling(test_case_num)
    
    async def run_test(self):
        await self.setup()
        test_cases = range(1, self.test_cases + 1)
        
        for i in range(0, len(test_cases), self.concurrent_users):
            group = test_cases[i:i + self.concurrent_users]
            tasks = [self.process_test_case(num) for num in group]
            await asyncio.gather(*tasks)

async def main():
    parser = argparse.ArgumentParser(description="LLM Load Testing Tool")
    parser.add_argument("concurrent_users", type=int, help="Number of concurrent users")
    parser.add_argument("test_cases", type=int, help="Number of test cases to run")
    
    args = parser.parse_args()
    tester = LLMTester(args.concurrent_users, args.test_cases)
    await tester.run_test()

if __name__ == "__main__":
    asyncio.run(main()) 