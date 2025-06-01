from qdrant_client import QdrantClient
from openai import OpenAI
import os
from dotenv import load_dotenv

def test_qdrant_connection():
    """Qdrant 서버 연결을 테스트합니다."""
    try:
        client = QdrantClient("localhost", port=6333)
        collections = client.get_collections()
        print("Qdrant 서버 연결 성공!")
        print("현재 컬렉션 목록:", [collection.name for collection in collections.collections])
        return True
    except Exception as e:
        print("Qdrant 서버 연결 실패:", str(e))
        return False

def test_openai_connection():
    """OpenAI API 연결을 테스트합니다."""
    try:
        # 환경 변수 확인
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("OpenAI API 키가 설정되지 않았습니다.")
            return False
        
        print(f"API 키 길이: {len(api_key)}")
        print(f"API 키 시작: {api_key[:10]}...")
        
        client = OpenAI()
        response = client.embeddings.create(
            input="테스트",
            model="text-embedding-ada-002"
        )
        print("OpenAI API 연결 성공!")
        return True
    except Exception as e:
        print("OpenAI API 연결 실패:", str(e))
        return False

if __name__ == "__main__":
    # 환경 변수 로드
    load_dotenv()
    
    print("=== 연결 테스트 시작 ===")
    
    # Qdrant 연결 테스트
    print("\n1. Qdrant 서버 연결 테스트")
    qdrant_ok = test_qdrant_connection()
    
    # OpenAI 연결 테스트
    print("\n2. OpenAI API 연결 테스트")
    openai_ok = test_openai_connection()
    
    print("\n=== 테스트 결과 요약 ===")
    print(f"Qdrant 서버: {'성공' if qdrant_ok else '실패'}")
    print(f"OpenAI API: {'성공' if openai_ok else '실패'}") 