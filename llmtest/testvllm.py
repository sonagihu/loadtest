import asyncio
import time
import json
import httpx
from typing import Dict, List, Optional
import pandas as pd
from datetime import datetime

class VLLMTest:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60.0
        )

    async def generate(
        self,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.95,
        stream: bool = False
    ) -> Dict:
        """
        vllm API를 통해 텍스트 생성을 수행합니다.
        """
        payload = {
            "model": "qwen3",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "stream": stream
        }

        print(f"\nAPI 요청 URL: {self.base_url}/chat/completions")
        print(f"API 요청 헤더: {self.client.headers}")
        print(f"API 요청 페이로드: {json.dumps(payload, ensure_ascii=False, indent=2)}")

        start_time = time.time()
        first_token_time = None
        try:
            response = await self.client.post("/chat/completions", json=payload)
            print(f"API 응답 상태 코드: {response.status_code}")
            print(f"API 응답 내용: {response.text}")
        except Exception as e:
            print(f"API 요청 중 오류 발생: {str(e)}")
            raise

        if response.status_code != 200:
            raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")

        result = response.json()
        
        # TTFT (Time To First Token) 계산
        if "usage" in result and "first_token_time" in result["usage"]:
            first_token_time = result["usage"]["first_token_time"]
        
        return {
            "response": result,
            "elapsed_time": time.time() - start_time,
            "ttft": first_token_time if first_token_time else None
        }

    async def run_test(
        self,
        prompts: List[str],
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.95
    ) -> pd.DataFrame:
        """
        여러 프롬프트에 대해 테스트를 실행하고 결과를 DataFrame으로 반환합니다.
        """
        results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"테스트 {i}/{len(prompts)} 실행 중...")
            try:
                result = await self.generate(
                    prompt=prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
                )
                
                results.append({
                    "prompt": prompt,
                    "elapsed_time": result["elapsed_time"],
                    "ttft": result["ttft"],
                    "response_length": len(result["response"].get("choices", [{}])[0].get("message", {}).get("content", "")),
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "prompt": prompt,
                    "elapsed_time": None,
                    "ttft": None,
                    "response_length": 0,
                    "status": f"error: {str(e)}"
                })
        
        return pd.DataFrame(results)

    async def close(self):
        """
        HTTP 클라이언트를 종료합니다.
        """
        await self.client.aclose()

    async def list_models(self):
        """
        /v1/models 엔드포인트에서 지원 모델 리스트를 조회합니다.
        """
        try:
            response = await self.client.get("/models")
            print(f"/v1/models 응답 상태 코드: {response.status_code}")
            print(f"/v1/models 응답 내용: {response.text}")
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"/v1/models 조회 중 오류 발생: {str(e)}")
            return None

async def main():
    # 테스트 설정
    base_url = "https://i1el6rswlamycy-8002.proxy.runpod.net/v1"
    api_key = "test"
    
    # VLLM 테스트 인스턴스 생성
    tester = VLLMTest(base_url, api_key)
    
    # # 모델 리스트 먼저 조회 (필요시 주석 해제)
    # print("\n서버에 등록된 모델 리스트를 조회합니다...")
    # await tester.list_models()

    # 테스트할 프롬프트 목록
    test_prompts = [
        "한국의 수도는?",
        "인공지능이란 무엇인가요?",
        "파이썬의 장점을 설명해주세요."
    ]
    try:
        # 테스트 실행
        results_df = await tester.run_test(test_prompts)
        # 결과 저장
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_df.to_csv(f"vllm_test_results_{timestamp}.csv", index=False)
        # 요약 통계 출력
        print("\n테스트 결과 요약:")
        print(f"총 테스트 수: {len(results_df)}")
        print(f"성공한 테스트 수: {len(results_df[results_df['status'] == 'success'])}")
        print("\n시간 측정 (초):")
        print(f"평균 응답 시간: {results_df['elapsed_time'].mean():.2f}")
        print(f"평균 TTFT: {results_df['ttft'].mean():.2f}")
    finally:
        await tester.close()

if __name__ == "__main__":
    asyncio.run(main()) 