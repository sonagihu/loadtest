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

class ResponseHandler:
    def __init__(self, result_dir: Path, summary_file: Path):
        self.result_dir = result_dir
        self.summary_file = summary_file
        self.response_queues = {}
        self.handlers = {}
        
    def start_handling(self, test_case_num: int, start_time: float):
        queue = Queue()
        self.response_queues[test_case_num] = queue
        
        def handle_response():
            response_file = self.result_dir / f"tc{test_case_num:03d}.res"
            first_response = True
            full_response = []
            
            while True:
                response = queue.get()
                if response is None:  # 종료 신호
                    break
                    
                if first_response:
                    elapsed_time = (time.time() - start_time) * 1000
                    with open(self.summary_file, "a", encoding="utf-8") as f:
                        f.write(f"tc{test_case_num:03d}.req,200,{elapsed_time:.2f}\n")
                    first_response = False
                
                if isinstance(response, dict) and "response" in response:
                    full_response.append(response["response"])
            
            # 전체 응답 저장
            with open(response_file, "w", encoding="utf-8") as f:
                f.write("".join(full_response))
        
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
            del self.response_queues[test_case_num]
            del self.handlers[test_case_num]

class LoadTester:
    def __init__(self, concurrent_users: int, test_cases: int):
        self.concurrent_users = concurrent_users
        self.test_cases = test_cases
        self.base_url = "http://localhost:11434/api/generate"
        self.request_dir = Path("request")
        self.response_dir = Path("response")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.result_dir = self.response_dir / self.timestamp
        self.summary_file = self.result_dir / "summary.txt"
        self.response_handler = ResponseHandler(self.result_dir, self.summary_file)
        
    async def setup(self):
        self.result_dir.mkdir(parents=True, exist_ok=True)
        with open(self.summary_file, "w", encoding="utf-8") as f:
            f.write("Test Case,Response Code,Elapsed Time (ms)\n")
    
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
    parser = argparse.ArgumentParser(description="Load Testing Tool")
    parser.add_argument("concurrent_users", type=int, help="Number of concurrent users")
    parser.add_argument("test_cases", type=int, help="Number of test cases to run")
    
    args = parser.parse_args()
    tester = LoadTester(args.concurrent_users, args.test_cases)
    await tester.run_test()

if __name__ == "__main__":
    asyncio.run(main()) 