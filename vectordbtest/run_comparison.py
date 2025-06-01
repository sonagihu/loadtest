import os
import time
from datetime import datetime
from vdbtest import run_load_test

def run_comparison(iterations: int = 100):
    """두 시나리오를 순차적으로 실행하고 결과를 비교합니다."""
    # 결과 저장 디렉토리 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = f"response/comparison_{timestamp}"
    os.makedirs(result_dir, exist_ok=True)
    
    print("\n=== 벡터 DB 검색 방식 비교 테스트 시작 ===")
    print(f"반복 횟수: {iterations}")
    print(f"결과 저장 디렉토리: {result_dir}")
    
    # req001 실행 (페이로드 필터링)
    print("\n1. 페이로드 필터링 검색 (req001) 실행 중...")
    start_time = time.time()
    run_load_test("req001", iterations)
    req001_time = time.time() - start_time
    
    # 잠시 대기
    time.sleep(2)
    
    # req002 실행 (인덱스 기반)
    print("\n2. 인덱스 기반 검색 (req002) 실행 중...")
    start_time = time.time()
    run_load_test("req002", iterations)
    req002_time = time.time() - start_time
    
    # 결과 요약 생성
    summary = f"""=== 벡터 DB 검색 방식 비교 결과 ===
테스트 시간: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
반복 횟수: {iterations}

=== 실행 시간 비교 ===
페이로드 필터링 (req001): {req001_time:.2f}초
인덱스 기반 (req002): {req002_time:.2f}초
성능 향상률: {(req001_time/req002_time - 1)*100:.1f}%

=== 상세 결과 ===
각 시나리오의 상세 결과는 다음 디렉토리에서 확인할 수 있습니다:
- req001: response/{timestamp}_req001
- req002: response/{timestamp}_req002
"""
    
    # 결과 저장
    with open(f"{result_dir}/comparison_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("\n=== 비교 테스트 완료 ===")
    print(f"결과가 {result_dir} 디렉토리에 저장되었습니다.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="벡터 DB 검색 방식 비교 테스트")
    parser.add_argument("--iterations", type=int, default=100,
                      help="각 시나리오의 반복 횟수 (기본값: 100)")
    
    args = parser.parse_args()
    run_comparison(args.iterations) 