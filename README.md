# Vector DB Load Test

이 프로젝트는 Qdrant 벡터 데이터베이스의 성능을 테스트하기 위한 부하 테스트 도구입니다.

## 기능

- Qdrant 벡터 DB 연결 및 컬렉션 생성
- Markdown 문서의 벡터 임베딩 및 저장
- 다양한 시나리오 기반 부하 테스트
- 성능 측정 및 결과 저장

## 요구사항

- Python 3.8 이상
- Qdrant 서버
- OpenAI API 키

## 설치

1. 저장소 클론:
```bash
git clone https://github.com/yourusername/loadtest.git
cd loadtest
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

## 사용 방법

1. Qdrant 서버 실행:
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

2. 컬렉션 생성:
```bash
python vectordbtest/create_collections.py
```

3. 문서 임베딩:
```bash
python vectordbtest/embed_documents.py
```

4. 부하 테스트 실행:
```bash
python vectordbtest/vdbtest.py --scenario req001 --iterations 100
```

## 시나리오

### req001: 파일명 기반 검색
- 파일명을 이용한 벡터 DB 검색 테스트
- 각 컬렉션별 실제 존재하는 파일만 검색
- 성능 측정 및 결과 저장

## 결과

테스트 결과는 `response/YYYYMMDD_HHMMSS/` 디렉토리에 저장됩니다:
- `summary.txt`: 전체 테스트 결과 요약
- `resXXX.txt`: 개별 응답 상세 정보

## 라이선스

MIT License 