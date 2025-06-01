from qdrant_client import QdrantClient
from qdrant_client.http import models
import time
import random
from typing import List, Dict, Any, Set, Tuple

class IndexedFileSearchScenario:
    def __init__(self):
        self.client = QdrantClient("localhost", port=6333)
        # 컬렉션별 파일 매핑 초기화
        self.collection_files: Dict[str, Set[str]] = {
            "service": {
                "CustomerController.md",
                "ProductController.md",
                "OrderController.md",
                "CustomerService.md",
                "ProductService.md",
                "OrderService.md"
            },
            "logic": {
                "Customer.md",
                "Product.md",
                "Order.md",
                "OrderItem.md",
                "CustomerRepository.md",
                "ProductRepository.md",
                "OrderRepository.md"
            }
        }
        
    def get_random_search_condition(self) -> Tuple[str, str]:
        """랜덤하게 검색 조건을 선택합니다."""
        # 랜덤하게 컬렉션 선택
        collection = random.choice(list(self.collection_files.keys()))
        # 선택된 컬렉션에서 랜덤하게 파일 선택
        filename = random.choice(list(self.collection_files[collection]))
        return filename, collection
        
    def search_by_filename(self, filename: str, collection_name: str) -> List[Dict[str, Any]]:
        """파일명으로 문서를 검색합니다."""
        try:
            # 필터 조건 설정 (인덱스된 필드 사용)
            filter_condition = models.Filter(
                must=[
                    models.FieldCondition(
                        key="filename",
                        match=models.MatchValue(value=filename)
                    )
                ]
            )
            
            # 검색 실행 (dummy vector로 검색)
            dummy_vector = [0.0] * 1536  # OpenAI embedding 차원
            search_result = self.client.search(
                collection_name=collection_name,
                query_vector=dummy_vector,
                query_filter=filter_condition,
                limit=1,
                search_params=models.SearchParams(
                    hnsw_ef=50,  # HNSW 인덱스 파라미터 조정
                    exact=False   # 근사 검색 사용
                )
            )
            
            return search_result
            
        except Exception as e:
            print(f"Error searching for {filename}: {str(e)}")
            return []
    
    def run_scenario(self, num_iterations: int = 100) -> Dict[str, Any]:
        """시나리오를 실행하고 성능을 측정합니다."""
        results = {
            "total_requests": num_iterations,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_time": 0,
            "avg_response_time": 0,
            "min_response_time": float('inf'),
            "max_response_time": 0,
            "response_times": [],
            "search_results": [],  # 검색 결과 저장
            "search_conditions": []  # 검색 조건 저장
        }
        
        print(f"\n=== 인덱스 기반 파일명 검색 시나리오 시작 (총 {num_iterations}회) ===")
        
        for i in range(num_iterations):
            # 랜덤하게 검색 조건 선택
            filename, collection = self.get_random_search_condition()
            
            # 검색 조건 저장
            search_condition = {
                "filename": filename,
                "collection": collection
            }
            results["search_conditions"].append(search_condition)
            
            start_time = time.time()
            
            try:
                # 검색 실행
                search_result = self.search_by_filename(filename, collection)
                results["search_results"].append(search_result)  # 검색 결과 저장
                
                if search_result:
                    results["successful_requests"] += 1
                else:
                    results["failed_requests"] += 1
                
                # 응답 시간 계산
                response_time = time.time() - start_time
                results["response_times"].append(response_time)
                results["total_time"] += response_time
                results["min_response_time"] = min(results["min_response_time"], response_time)
                results["max_response_time"] = max(results["max_response_time"], response_time)
                
                if (i + 1) % 10 == 0:
                    print(f"진행률: {i + 1}/{num_iterations} ({(i + 1)/num_iterations*100:.1f}%)")
                
            except Exception as e:
                results["failed_requests"] += 1
                results["search_results"].append([])  # 실패한 경우 빈 결과 저장
                print(f"Error in iteration {i + 1}: {str(e)}")
        
        # 평균 응답 시간 계산
        if results["successful_requests"] > 0:
            results["avg_response_time"] = results["total_time"] / results["successful_requests"]
        
        # 결과 출력
        print("\n=== 시나리오 실행 결과 ===")
        print(f"총 요청 수: {results['total_requests']}")
        print(f"성공한 요청 수: {results['successful_requests']}")
        print(f"실패한 요청 수: {results['failed_requests']}")
        print(f"평균 응답 시간: {results['avg_response_time']*1000:.2f}ms")
        print(f"최소 응답 시간: {results['min_response_time']*1000:.2f}ms")
        print(f"최대 응답 시간: {results['max_response_time']*1000:.2f}ms")
        
        return results

if __name__ == "__main__":
    # 시나리오 인스턴스 생성
    scenario = IndexedFileSearchScenario()
    # 시나리오 실행 (100회 반복)
    results = scenario.run_scenario(100) 