"""
🎯 FastAPI 실습: HuggingFace 요약 모델 서빙
1. Lifespan을 활용한 HuggingFace Transformers 모델 로딩
2. Pydantic BaseModel을 사용한 요청 데이터 검증
3. POST 요청으로 텍스트 요약 API 구현
4. HTTPException을 활용한 에러 처리

📌 개발 환경 실행(로컬 테스트):
uvicorn lab1.hf_summary_en:app 
또는
python ./lab1/hf_summary_en.py

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from transformers import pipeline

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("======= 요약모델 로딩중 ...")
    ml_models["summarizer"] = pipeline("summarization", model="sentiment-analysis")
    ml_models['sentiment'] = pipeline(model="sentiment-analysis")
    print("✅ 모델 로딩 완료!")
    yield
    ml_models.clear()

app = FastAPI(lifespan=lifespan)

class ArticleRequest(BaseModel):
    text: str
    style: str = "medium"
    min_length: int = 30        # 최소 길이 설정 가능
    max_length: int = 200       # 최대 길이 설정 가능


@app.post("/summarize")
def summarize_text(request: ArticleRequest):
    summarizer = ml_models["summarizer"]


    if request.style == "short":
        request.min_length = 20
        request.max_length = 50
    elif request.style == "medium":
        request.min_length = 50
        request.max_length = 150
    else:
        request.min_length = 100
        request.max_length = 300


    if len(request.text) < 50 :
        raise HTTPException(status_code=400, detail="텍스트가 너무 짧습니다.")
    
    try:
        result = summarizer(
            request.text,
            max_length=request.max_length,
            min_length=request.min_length
        )
        return {"summary": result[0]['summary_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":      # 이 파일을 직접 실행할 때만 아래 코드를 실행하고, import될 때는 실행하지 않음
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
