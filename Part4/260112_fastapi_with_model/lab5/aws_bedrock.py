"""
🎯 FastAPI 실습: AWS Bedrock + Claude 3 광고 문구 생성기
1. boto3를 사용한 AWS Bedrock 클라이언트 설정
2. Claude 3 (Haiku) 모델 호출 및 응답 파싱
3. 프롬프트 엔지니어링으로 마케터 역할 부여
4. OpenAI API 대신 AWS 기반 LLM 서빙 패턴 이해

📌 사전 준비:
1. pip install fastapi uvicorn boto3 python-dotenv
2. AWS 계정에서 Bedrock 모델 액세스 활성화 (Claude 3 Haiku)
3. .env 파일 설정:
   AWS_ACCESS_KEY=AKIA...
   AWS_SECRET_KEY=...
   (AWS IAM에서 AmazonBedrockFullAccess 권한 필요)

📌 실행 방법:
python ./lab5/aws_bedrock.py

💡 OpenAI vs AWS Bedrock 비교:
┌─────────────┬──────────────────┬──────────────────┐
│             │ OpenAI API       │ AWS Bedrock      │
├─────────────┼──────────────────┼──────────────────┤
│ 인증         │ API Key          │ IAM (Access/Secret)│
│ 클라이언트     │ openai 라이브러리   │ boto3            │
│ 모델        │ gpt-4o-mini 등     │ Claude, Titan 등 │
│ 과금        │ OpenAI 직접 결제     │ AWS 청구서 통합    │
│ 보안        │ API Key 관리        │ IAM 정책 관리    │
└─────────────┴──────────────────┴──────────────────┘

💡 Bedrock 모델 ID 예시:
- anthropic.claude-3-haiku-20240307-v1:0 (빠름, 저렴)
- anthropic.claude-3-sonnet-20240229-v1:0 (균형)
- anthropic.claude-3-opus-20240229-v1:0 (고성능)

⚠️ 주의사항:
- AWS 리전별로 사용 가능한 모델이 다름 (us-east-1 권장)
- Bedrock 콘솔에서 모델 액세스 요청 필요 (승인까지 몇 분 소요)
- IAM 사용자에게 AmazonBedrockFullAccess 정책 연결 필요
"""

import json
import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = FastAPI()

# --------------------------------------------------------
# 1. AWS Bedrock 클라이언트 설정
# --------------------------------------------------------
# 실습용: 본인의 AWS Access Key와 Secret Key를 여기에 체크합니다.
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_REGION = "us-east-1"                # Bedrock 모델이 활성화된 리전 (예: us-east-1, us-west-2)

api_key=os.getenv("OPENAI_API_KEY")

# boto3 클라이언트 생성 (boto3가 AWS와 통신합니다)
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

# 2. 데이터 모델 정의 (Pydantic)
# --------------------------------------------------------
class AdRequest(BaseModel):
    product_name: str   # 예: "초경량 무선 청소기"
    keywords: str       # 예: "강력한 흡입력, 조용함, 가벼움"

# 3. API 엔드포인트 정의
# --------------------------------------------------------
@app.post("/generate-ad")
async def generate_ad_copy(request: AdRequest):
    try:
        # (1) 프롬프트 작성: AI에게 지시할 내용을 만듭니다.
        prompt = f"""
        당신은 전문 마케터입니다. 아래 제품에 대한 매력적인 SNS 광고 문구를 3줄 이내로 작성해주세요.
        
        
        제품명: {request.product_name}
        강조할 키워드: {request.keywords}
        
        광고 문구:
        """

        # (2) Bedrock (Claude 3) 요청 바디 구성
        # Claude 3는 'messages' 형식을 사용합니다.
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 500,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        })

        # (3) 모델 호출 (invoke_model)
        # ========== modelId는 AWS 콘솔에서 확인 가능 (여기선 Claude 3 Haiku 사용) =========
        model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        
        response = bedrock_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )

        # (4) 응답 파싱
        response_body = json.loads(response.get("body").read())
        result_text = response_body['content'][0]['text']

        return {"result": result_text}

    except Exception as e:
        # 에러 발생 시 상세 내용 반환
        raise HTTPException(status_code=500, detail=str(e))

# 서버 실행 테스트를 위한 기본 루트
@app.get("/")
def read_root():
    return {"message": "AWS Bedrock FastAPI 서비스가 실행 중입니다!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)