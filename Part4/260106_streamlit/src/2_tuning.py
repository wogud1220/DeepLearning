#####################################################################
# 실습 2: Form & Session State
# Streamlit은 상호작용 시마다 코드가 재실행되므로 변수가 초기화됩니다.
# 이를 방지하는 Session State와, 설정을 한 번에 전송하는 Form 사용
#####################################################################
import streamlit as st
import time
import random
import pandas as pd

st.title("🧪 하이퍼파라미터 튜닝 시뮬레이터")

# [Session State] 실험 기록 저장소 초기화 
# 페이지가 새로고침 되어도 리스트가 사라지지 않고 유지됩니다.
if 'history' not in st.session_state:
    st.session_state.history = []

# [Form] 입력 양식 (버튼 누르기 전까지 실행 방지) 
with st.form("training_form"):
    st.subheader("모델 파라미터 설정")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        learning_rate = st.slider("Learning Rate", 0.001, 0.1, 0.01) 
    with col2:
        epochs = st.slider("Epochs", 1, 100, 10)
    with col3:
        batch_size = st.selectbox("Batch Size", options=[16, 32, 64, 128])
    
    # 폼 제출 버튼 
    submitted = st.form_submit_button("학습 시작")

# 학습 로직 실행
if submitted:
    st.write(f"학습 시작... (LR: {learning_rate}, Epochs: {epochs})")
    
    # 진행률 표시 바 
    progress_bar = st.progress(0)
    status_text = st.empty() # 텍스트를 업데이트하기 위한 자리표시자, 갱신됨
    # write 쓰면 축적됨

    # 가상의 학습 과정 시뮬레이션
    for i in range(100):
        time.sleep(0.01) # 0.01초 대기
        progress_bar.progress(i + 1)
        status_text.text(f"Progress: {i+1}%")
    
    # 결과 생성 (랜덤)
    accuracy = random.uniform(0.70, 0.99)
    loss = random.uniform(0.1, 0.5)
    
    st.success(f"학습 완료! Accuracy: {accuracy:.4f}")
    
    # [Session State] 결과 저장 
    # 이전 실험 결과들에 현재 결과를 추가함
    st.session_state.history.append({
        "Learning Rate": learning_rate,
        "Epochs": epochs,
        "Batch Size": batch_size,
        "Accuracy": accuracy,
        "Loss": loss
    })

# 저장된 실험 기록 출력
if len(st.session_state.history) > 0:
    st.markdown("---")
    st.subheader("📝 실험 기록 (Session State 유지)")
    # 리스트를 데이터프레임으로 변환하여 표로 출력
    st.dataframe(pd.DataFrame(st.session_state.history))

if len(st.session_state.history) > 0:
    st.markdown("---")
    st.subheader("line chart")
    df = pd.DataFrame(st.session_state.history)
    st.line_chart(df['Accuracy'])

with st.sidebar:
    if st.button("Reset Session State"):
        st.session_state.history = []
        st.rerun()

