# Vector DB & LLM Load Test Project

이 프로젝트는 Qdrant 벡터 데이터베이스의 다양한 검색 방식과 LLM(Large Language Model)의 성능을 테스트하는 도구입니다.

## 프로젝트 구조

```
loadtest/
├── vectordbtest/              # 벡터 DB 테스트 관련 코드
│   ├── request/              # 테스트 시나리오
│   │   ├── req001.py        # 페이로드 필터링 검색 시나리오
│   │   └── req002.py        # 인덱스 기반 검색 시나리오
│   ├── codesample/          # 테스트용 샘플 코드
│   │   └── shoppingmall/    # 쇼핑몰 예제 코드
│   ├── response/            # 테스트 결과 저장 디렉토리
│   ├── embed_documents.py   # 문서 임베딩 및 저장
│   ├── vdbtest.py          # 부하 테스트 실행
│   ├── run_comparison.py   # 검색 방식 비교 테스트
│   └── test_connection.py  # 연결 테스트
├── llmtest/                 # LLM 테스트 관련 코드
│   ├── request/            # LLM 테스트 시나리오
│   │   ├── req001.py      # 기본 프롬프트 테스트
│   │   └── req002.py      # 체인 프롬프트 테스트
│   ├── response/          # LLM 테스트 결과 저장
│   └── llmtest.py        # LLM 부하 테스트 실행
├── docker-compose.yml      # Qdrant 서버 설정
└── requirements.txt        # 프로젝트 의존성
```

## 주요 기능

### 1. 벡터 DB 테스트
#### 1.1 문서 임베딩 및 저장
- Java 소스 코드를 Markdown으로 변환
- OpenAI API를 사용한 텍스트 임베딩
- Qdrant 벡터 DB에 저장
- 컬렉션별 인덱스 설정

#### 1.2 검색 시나리오
- **req001**: 페이로드 필터링 기반 검색
  - 파일명으로 문서 검색
  - 필터 조건을 통한 정확한 매칭
- **req002**: 인덱스 기반 검색
  - HNSW 인덱스 활용
  - 최적화된 검색 파라미터 사용

### 2. LLM 테스트
#### 2.1 프롬프트 시나리오
- **req001**: 기본 프롬프트 테스트
  - 단일 프롬프트 처리
  - 응답 시간 및 토큰 사용량 측정
- **req002**: 체인 프롬프트 테스트
  - 다단계 프롬프트 처리
  - 컨텍스트 유지 및 전달 테스트

#### 2.2 성능 측정
- 토큰 처리 속도
- 응답 생성 시간
- 컨텍스트 처리 효율성
- 에러율 및 재시도 통계

### 3. 성능 테스트
- 개별 시나리오 테스트
- 검색/프롬프트 방식 비교 테스트
- 응답 시간 측정
- 성공/실패 요청 통계

## 설치 및 설정

### 1. 환경 요구사항
- Python 3.8 이상
- Docker
- OpenAI API 키

### 2. 설치 방법
```bash
# 저장소 클론
git clone https://github.com/sonagihu/loadtest.git
cd loadtest

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt

# OpenAI API 키 설정
export OPENAI_API_KEY="your-api-key"  # Linux/Mac
set OPENAI_API_KEY="your-api-key"     # Windows
```

### 3. Qdrant 서버 실행
```bash
docker-compose up -d
```

## 사용 방법

### 1. 벡터 DB 테스트
```bash
# 문서 임베딩
python vectordbtest/embed_documents.py

# 페이로드 필터링 검색
python vectordbtest/vdbtest.py --scenario req001 --iterations 100

# 인덱스 기반 검색
python vectordbtest/vdbtest.py --scenario req002 --iterations 100

# 검색 방식 비교
python vectordbtest/run_comparison.py --iterations 100
```

### 2. LLM 테스트
```bash
# 기본 프롬프트 테스트
python llmtest/llmtest.py --scenario req001 --iterations 100

# 체인 프롬프트 테스트
python llmtest/llmtest.py --scenario req002 --iterations 100
```

## 테스트 결과

### 벡터 DB 테스트 결과
`vectordbtest/response/` 디렉토리에 저장:
- `summary.txt`: 전체 테스트 요약
- `res*.txt`: 개별 요청 결과
- `comparison_summary.txt`: 검색 방식 비교 결과

### LLM 테스트 결과
`llmtest/response/` 디렉토리에 저장:
- `summary.txt`: 전체 테스트 요약
- `res*.txt`: 개별 요청 결과
- `token_usage.txt`: 토큰 사용량 통계
- `performance_metrics.txt`: 성능 지표

## 주요 기술 스택

- **벡터 DB**: Qdrant
- **LLM**: OpenAI API (GPT-4, GPT-3.5-turbo)
- **임베딩**: OpenAI API (text-embedding-3-small)
- **컨테이너화**: Docker
- **프로그래밍 언어**: Python 3.8+
- **의존성 관리**: pip

## 라이선스

MIT License

## 기여 방법

1. 이슈 생성
2. 브랜치 생성
3. 변경사항 커밋
4. Pull Request 생성

## 연락처

프로젝트 관리자: [GitHub 프로필](https://github.com/sonagihu) 