#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import time
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import argparse
from request.req001 import FileSearchScenario

class VectorDBLoadTest:
    def __init__(self, concurrent_users: int, test_cases: int):
        self.concurrent_users = concurrent_users
        self.test_cases = test_cases
        self.results_dir = self._create_results_dir()
        
    def _create_results_dir(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_dir = os.path.join("response", timestamp)
        os.makedirs(results_dir, exist_ok=True)
        return results_dir

    async def run_test(self):
        print(f"VectorDB 부하 테스트 시작: {self.concurrent_users}명의 동시 사용자, {self.test_cases}개의 테스트 케이스")
        # TODO: 실제 테스트 로직 구현
        pass

def save_response(results_dir: str, response_num: int, content: str):
    """개별 응답을 파일로 저장합니다."""
    filename = f"res{response_num:03d}.txt"
    filepath = os.path.join(results_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def save_summary(results_dir: str, summary: str):
    """요약 정보를 파일로 저장합니다."""
    filepath = os.path.join(results_dir, "summary.txt")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(summary)

def run_load_test(scenario_name: str, iterations: int = 100):
    """부하 테스트를 실행합니다."""
    # 결과 디렉토리 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = os.path.join("response", timestamp)
    os.makedirs(results_dir, exist_ok=True)
    
    print(f"\n=== 부하 테스트 시작: {datetime.now()} ===")
    print(f"시나리오: {scenario_name}")
    print(f"반복 횟수: {iterations}")
    
    start_time = time.time()
    
    if scenario_name == "req001":
        scenario = FileSearchScenario()
        results = scenario.run_scenario(iterations)
    else:
        print(f"알 수 없는 시나리오: {scenario_name}")
        return
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # 결과 요약 생성
    summary = f"""=== 부하 테스트 결과 요약 ===
테스트 시작: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
시나리오: {scenario_name}
반복 횟수: {iterations}

=== 성능 지표 ===
총 실행 시간: {total_time:.2f}초
초당 처리량: {iterations/total_time:.2f} req/s

=== 상세 결과 ===
총 요청 수: {results['total_requests']}
성공한 요청 수: {results['successful_requests']}
실패한 요청 수: {results['failed_requests']}
평균 응답 시간: {results['avg_response_time']*1000:.2f}ms
최소 응답 시간: {results['min_response_time']*1000:.2f}ms
최대 응답 시간: {results['max_response_time']*1000:.2f}ms
"""
    
    # 결과 출력
    print("\n=== 부하 테스트 완료 ===")
    print(f"총 실행 시간: {total_time:.2f}초")
    print(f"초당 처리량: {iterations/total_time:.2f} req/s")
    
    # 결과 저장
    save_summary(results_dir, summary)
    
    # 각 응답 저장
    for i, (response_time, search_result, search_condition) in enumerate(zip(
        results['response_times'], 
        results['search_results'],
        results['search_conditions']
    ), 1):
        response_content = f"""=== 응답 {i} ===
검색 조건:
- 파일명: {search_condition['filename']}
- 컬렉션: {search_condition['collection']}
응답 시간: {response_time*1000:.2f}ms

=== 검색 결과 ===
"""
        if search_result:
            for idx, result in enumerate(search_result, 1):
                response_content += f"""
결과 {idx}:
- 점수: {result.score:.4f}
- 파일명: {result.payload.get('filename', 'N/A')}
- 디렉토리: {result.payload.get('directory', 'N/A')}
- 내용: {result.payload.get('content', 'N/A')[:200]}...
"""
        else:
            response_content += "검색 결과 없음\n"
            
        save_response(results_dir, i, response_content)
    
    print(f"\n결과가 {results_dir} 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Vector DB 부하 테스트')
    parser.add_argument('--scenario', type=str, default='req001',
                      help='실행할 시나리오 이름 (예: req001)')
    parser.add_argument('--iterations', type=int, default=100,
                      help='반복 횟수 (기본값: 100)')
    
    args = parser.parse_args()
    
    run_load_test(args.scenario, args.iterations) 