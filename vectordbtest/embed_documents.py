import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import hashlib

# 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
openai_client = OpenAI()

# Qdrant 클라이언트 초기화
qdrant_client = QdrantClient("localhost", port=6333)

def create_collection(collection_name: str):
    """컬렉션을 생성하고 필요한 인덱스를 설정합니다."""
    try:
        # 벡터 설정
        vectors_config = models.VectorParams(
            size=1536,  # OpenAI embedding 차원
            distance=models.Distance.COSINE
        )
        
        # 최적화 설정
        optimizers_config = models.OptimizersConfigDiff(
            indexing_threshold=0,  # 즉시 인덱싱
            memmap_threshold=20000  # 메모리 매핑 임계값
        )
        
        # 컬렉션 생성
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
            optimizers_config=optimizers_config
        )
        
        # filename 필드에 대한 인덱스 생성
        qdrant_client.create_payload_index(
            collection_name=collection_name,
            field_name="filename",
            field_schema=models.PayloadFieldSchema.KEYWORD
        )
        
        print(f"Created collection '{collection_name}' with filename index")
        
    except Exception as e:
        print(f"Error creating collection '{collection_name}': {str(e)}")

def get_embedding(text):
    """OpenAI API를 사용하여 텍스트의 임베딩을 생성합니다."""
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding

def read_md_file(file_path):
    """MD 파일의 내용을 읽어옵니다."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def generate_point_id(file_path):
    """파일 경로를 기반으로 양의 정수 ID를 생성합니다."""
    # 파일 경로의 해시값을 생성
    hash_object = hashlib.md5(str(file_path).encode())
    # 해시값의 첫 8바이트를 정수로 변환하고 절대값을 취함
    return abs(int.from_bytes(hash_object.digest()[:8], byteorder='big'))

def process_directory(directory, collection_name):
    """디렉토리 내의 모든 MD 파일을 처리하여 지정된 컬렉션에 임베딩합니다."""
    base_path = Path("codesample/shoppingmall")
    dir_path = base_path / directory
    
    for file_path in dir_path.glob("*.md"):
        try:
            # 파일 내용 읽기
            content = read_md_file(file_path)
            
            # 임베딩 생성
            embedding = get_embedding(content)
            
            # 메타데이터 준비
            metadata = {
                "filename": file_path.name,
                "directory": directory,
                "content": content
            }
            
            # 포인트 ID 생성
            point_id = generate_point_id(file_path)
            
            # Qdrant에 저장
            qdrant_client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload=metadata
                    )
                ]
            )
            print(f"Processed: {file_path} -> {collection_name}")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")

def main():
    # 컬렉션 생성
    create_collection("service")
    create_collection("logic")
    
    # service 컬렉션에 controller와 service 디렉토리의 파일 임베딩
    process_directory("controller", "service")
    process_directory("service", "service")

    # logic 컬렉션에 bean과 dbio 디렉토리의 파일 임베딩
    process_directory("bean", "logic")
    process_directory("dbio", "logic")

    print("모든 파일이 성공적으로 임베딩되었습니다.")

if __name__ == "__main__":
    main() 