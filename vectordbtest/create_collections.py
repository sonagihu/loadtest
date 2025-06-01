from qdrant_client import QdrantClient
from qdrant_client.http import models

# Qdrant 클라이언트 초기화
client = QdrantClient("localhost", port=6333)

# 컬렉션 설정
vector_size = 1536  # OpenAI의 text-embedding-ada-002 모델의 임베딩 크기

# service 컬렉션 생성
client.create_collection(
    collection_name="service",
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
)

# logic 컬렉션 생성
client.create_collection(
    collection_name="logic",
    vectors_config=models.VectorParams(
        size=vector_size,
        distance=models.Distance.COSINE
    )
)

print("컬렉션이 성공적으로 생성되었습니다.") 