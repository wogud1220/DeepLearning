#####################################################################
# FastAPI 서버가 될 부분
#####################################################################

import random

class MyModel:
    def __init__(self):
        # 실제 모델이라면 여기서 가중치를 로드합니다.
        print("Model initialized")

    def predict(self, input_text, keywords):
        # AI 예측 로직 시뮬레이션
        # 나중에 이 부분만 FastAPI의 엔드포인트 함수로 변경하면 됩니다.

        if any(word in input_text for word in keywords):
            is_spam = True
            reason_spam = "금지어가 포함되어 있습니다."
        else:
            is_spam = False
            reason_spam = "특이사항 없음."


        return {
            "input": input_text,
            "score": is_spam,
            "reason": reason_spam
        }