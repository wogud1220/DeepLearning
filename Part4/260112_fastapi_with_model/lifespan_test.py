"""
🎯 FastAPI 실습: Lifespan 
1. Lifespan을 활용한 서버 시작/종료 시 리소스 관리
2. ML 모델을 서버 시작 시 1회만 로딩하는 패턴 이해
3. 전역 저장소를 활용한 모델 공유 방식 학습

📌 실행 방법:
uvicorn lab0/lifespan_test:app --reload
"""
import asyncio
import os

# https://fastapi.tiangolo.com/advanced/events/
from fastapi import FastAPI
from contextlib import asynccontextmanager
import time
from dotenv import load_dotenv
load_dotenv()
# ===============================
# Fake model loader
# ===============================
async def load_model():
    await asyncio.sleep(float(os.getenv('MODEL_LOAD_TIME')))
    return {"model": "fake-ml-model",
            "model2": "fake-translator"}
# ===============================
# 전역 모델 저장소
# ===============================
ml_models = {}  # global dict

# ===============================
# Lifespan: 서버 시작/종료 시 리소스 관리
# ===============================
# yield를 기준으로 쓸 것이다.
@asynccontextmanager                # ① 비동기 컨텍스트 매니저로 만들어주는 데코레이터
async def lifespan(app: FastAPI):
    # ② 서버 시작 시 실행되는 부분 (startup)
    print(time.time())
    print("====== 모델로딩중...")
    ml_models['sentiment'], ml_models['translator'] = await asyncio.gather(
        load_model(),
        load_model()
    )
    print("✅ 모델 로딩 완료")
    print(time.time())

    # ③ 여기서 "일시정지" → 서버가 요청을 받기 시작
    yield

    # ④ 서버 종료 시 실행되는 부분 (shutdown)
    print("🧹 모델 메모리 정리")
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


# ===============================
# API Endpoints
# ===============================
@app.get("/predict/sentiment")
def predict(text: str):
    model = ml_models["sentiment"]
    return {
        "input": text,
        "prediction": "positive",
        "model": model["model"]
    }

@app.get("/predict/translate")
def predict2(text: str):
    model = ml_models["translator"]
    return {
        "input": text,
        "prediction": "positive",
        "model": model["model2"]
    }

@app.get("/bad")
def bad_example(text: str):
    print("- 모델 매번 로딩 X")
    model = load_model()
    return {
        "input": text,
        "result": "느림",
        "model": model["model"]
    }
