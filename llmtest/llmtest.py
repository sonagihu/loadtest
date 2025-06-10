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
from typing import Dict, List
import re

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

class VLLMTest:
    def __init__(self, base_url: str, api_key: str, concurrent_users: int, test_cases: int, length: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = "qwen3"
        self.concurrent_users = concurrent_users
        self.test_cases = test_cases
        self.length = length.upper()  # S, M, L 중 하나
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.result_dir = Path("response") / self.timestamp
        self.summary_file = self.result_dir / "summary.csv"
        self.success_count = 0
        self.total_count = 0
        self.total_ttft = 0
        self.total_tbt = 0
        self.total_elapsed_time = 0
        
    def get_test_case_files(self) -> List[str]:
        """테스트 케이스 파일 목록을 가져오고 길이에 따라 필터링합니다."""
        request_dir = Path("request")
        test_files = []
        
        # 모든 .req 파일을 가져옴
        for file in request_dir.glob("*.req"):
            # 파일명의 3번째 자리 문자로 길이 판단 (예: CT_S_B_001.req -> S)
            if len(file.name) >= 4:
                file_length = file.name.split('_')[1].upper()
                if file_length == self.length:
                    test_files.append(file.name)
        
        return sorted(test_files)
    
    async def setup(self):
        self.result_dir.mkdir(parents=True, exist_ok=True)
        with open(self.summary_file, "w", encoding="utf-8") as f:
            f.write("Test Case,Response Code,Start Time,TTFT(ms),TBT(ms),Elapsed Time(ms),Total Res Tokens\n")
    
    async def process_test_case(self, test_case_file: str):
        test_case_path = Path("request") / test_case_file
        
        if not test_case_path.exists():
            print(f"테스트 케이스 파일이 존재하지 않습니다: {test_case_file}")
            return
        
        with open(test_case_path, "r", encoding="utf-8") as f:
            request_data = f.read().strip()
        
        start_time = time.time()
        result = await self.generate(request_data)
        end_time = time.time()
        
        # 테스트 케이스 번호 추출 (CT_S_B_001.req -> 1)
        test_case_num = int(test_case_file.split('_')[-1].split('.')[0])
        
        # 응답 저장
        response_file = self.result_dir / test_case_file.replace('.req', '.res')
        with open(response_file, "w", encoding="utf-8") as f:
            f.write(result["response"])
        
        # 시간 측정 및 통계 업데이트
        elapsed_time = (end_time - start_time) * 1000  # ms 단위로 변환
        self.total_count += 1
        if result["response"]:
            self.success_count += 1
            self.total_elapsed_time += elapsed_time
            self.total_ttft += result.get("ttft", elapsed_time)
            self.total_tbt += result.get("tbt", 0)
        
        # 요약 정보 기록
        start_time_str = datetime.fromtimestamp(start_time).strftime('%H%M%S.%f')[:-4]
        with open(self.summary_file, "a", encoding="utf-8") as f:
            f.write(f"{test_case_file},200,{start_time_str},{result.get('ttft', elapsed_time):.2f},{result.get('tbt', 0):.2f},{elapsed_time:.2f},{len(result['response'])}\n")
        
        print(f"테스트 케이스 {test_case_file} 응답: {result['response'][:100]}...")
    
    async def run_test(self):
        await self.setup()
        
        # 선택된 길이에 해당하는 테스트 케이스 파일 목록 가져오기
        test_files = self.get_test_case_files()
        if not test_files:
            print(f"선택한 길이({self.length})에 해당하는 테스트 케이스가 없습니다.")
            return
        
        # 테스트 케이스 수만큼만 선택
        test_files = test_files[:self.test_cases]
        
        async def user_task(user_id: int):
            print(f"사용자 {user_id} 시작")
            for test_file in test_files:
                await self.process_test_case(test_file)
            print(f"사용자 {user_id} 완료")
        
        # 각 사용자(스레드)가 모든 테스트 케이스를 실행
        tasks = [user_task(user_id) for user_id in range(1, self.concurrent_users + 1)]
        await asyncio.gather(*tasks)
        
        # 최종 요약 정보 출력
        avg_ttft = self.total_ttft / self.success_count if self.success_count > 0 else 0
        avg_tbt = self.total_tbt / self.success_count if self.success_count > 0 else 0
        avg_elapsed_time = self.total_elapsed_time / self.success_count if self.success_count > 0 else 0
        
        with open(self.summary_file, "a", encoding="utf-8") as f:
            f.write(f"\n정상건수/전체건수: {self.success_count}/{self.total_count}\n")
            f.write(f"평균 TTFT: {avg_ttft:.2f}ms\n")
            f.write(f"평균 TBT: {avg_tbt:.2f}ms\n")
            f.write(f"평균 Elapsed Time: {avg_elapsed_time:.2f}ms\n")
        
        print("\n테스트 완료")
        print(f"정상건수/전체건수: {self.success_count}/{self.total_count}")
        print(f"평균 TTFT: {avg_ttft:.2f}ms")
        print(f"평균 TBT: {avg_tbt:.2f}ms")
        print(f"평균 Elapsed Time: {avg_elapsed_time:.2f}ms")

    async def generate(self, prompt: str) -> Dict:
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 2048,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "stream": False
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    end_time = time.time()
                    return {
                        "response": data["choices"][0]["message"]["content"],
                        "ttft": (end_time - start_time) * 1000,  # ms 단위로 변환
                        "tbt": (end_time - start_time) * 1000 / len(data["choices"][0]["message"]["content"].split()) if data["choices"][0]["message"]["content"] else 0
                    }
                else:
                    return {"response": "", "ttft": 0, "tbt": 0}

async def main():
    parser = argparse.ArgumentParser(description="LLM Load Testing Tool")
    parser.add_argument("--user", type=int, default=1, help="동시 사용자 수")
    parser.add_argument("--tc", type=int, default=1, help="테스트 시나리오 수")
    parser.add_argument("--len", type=str, default="M", choices=["S", "M", "L"], help="테스트 케이스 길이 (S: Short, M: Medium, L: Long)")
    args = parser.parse_args()
    
    base_url = "https://i1el6rswlamycy-8002.proxy.runpod.net/v1"
    api_key = "test"
    concurrent_users = args.user
    test_cases = args.tc
    length = args.len
    tester = VLLMTest(base_url, api_key, concurrent_users, test_cases, length)
    await tester.run_test()

if __name__ == "__main__":
    asyncio.run(main()) 