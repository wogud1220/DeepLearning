#####################################################################
# 실습 4: 구조화 (FastAPI 연동 준비)
# 코드를 기능별로 분리하는 패턴
# model.py는 순수 파이썬 로직이므로, 나중에 FastAPI로 옮기기 매우 쉽습니다
#####################################################################
import streamlit as st
from model_4 import MyModel  # 분리된 로직 파일 import

st.set_page_config(page_title="구조화된 AI 앱", page_icon="🏗️")

st.title("🏗️ 구조화된 AI 앱 (FastAPI 준비)")
st.info("UI 코드와 모델 로직(model.py)을 분리하여 개발하는 패턴입니다.")

# [Caching] 클래스 인스턴스도 캐싱 가능
@st.cache_resource
def get_model_instance():
    return MyModel()

model = get_model_instance()

with st.sidebar:
    spam_words = st.text_input("금지어 설정 (쉼표로 구분)", value="광고, 무료")


# 쉼표 기준으로 분리 + 공백 제거
keywords = [k.strip() for k in spam_words.split(",") if k.strip()]

# UI 구성
text = st.text_input("스팸 메일인지 테스트할 문장 입력")

if st.button("검사"):
    # 분리된 model.py의 함수 호출
    result = model.predict(text, keywords)
    
    st.json(result) # 결과를 JSON 형태로 출력
    
    if result['score']:
        st.warning("스팸일 확률이 높습니다!")
        st.write(result['reason'])
    else:
        st.success("정상적인 메시지입니다.")