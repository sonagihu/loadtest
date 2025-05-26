# LLM Load Testing Tool

이 도구는 Ollama API 서버의 성능을 테스트하기 위한 로드 테스트 도구입니다. 동시 사용자 시뮬레이션과 응답 시간 측정을 통해 LLM 서버의 성능을 분석할 수 있습니다.

## 주요 기능

- 동시 사용자 시뮬레이션
- 비동기 요청 처리
- 스트리밍 응답 처리
- 응답 시간 측정 (첫 응답 도착 시간 기준)
- 테스트 결과 자동 저장

## 설치 방법

1. Python 3.7 이상이 필요합니다.
2. 필요한 패키지를 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```

## 사용 방법

```bash
python loadtest.py <동시_사용자_수> <테스트_케이스_수>
```

예시:
```bash
python loadtest.py 5 10  # 5명의 동시 사용자가 10개의 테스트 케이스를 실행
```

## 프로젝트 구조

```
llmtest/
├── request/           # 테스트 케이스 파일 디렉토리
│   ├── tc001.req
│   ├── tc002.req
│   └── ...
├── response/          # 테스트 결과 저장 디렉토리
│   └── YYYYMMDD_HHMMSS/
│       ├── summary.txt
│       ├── tc001.res
│       └── ...
├── loadtest.py        # 메인 스크립트
├── requirements.txt   # 의존성 파일
└── README.md         # 프로젝트 문서
```

## 결과

- 테스트 결과는 `response/<timestamp>` 디렉토리에 저장됩니다.
- `summary.txt` 파일에 각 테스트 케이스의 응답 코드와 경과 시간이 기록됩니다.
- 각 테스트 케이스의 응답은 `<timestamp>/tcXXX.res` 파일에 저장됩니다.

## 주의사항

- Ollama API 서버가 `http://localhost:11434`에서 실행 중이어야 합니다.
- 테스트 케이스 파일은 `request` 디렉토리에 `tc001.req`부터 순차적으로 존재해야 합니다.
- 각 테스트 케이스 파일은 Ollama API에 전달될 프롬프트를 포함해야 합니다.

## 라이선스

MIT License 