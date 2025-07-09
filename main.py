import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# -----------------------
# 타이틀
# -----------------------
st.title("📚 나의 학업 피드백 대시보드")
st.write("학습 내용을 기록하고 시각적으로 피드백을 받아보세요.")

# -----------------------
# 입력 폼
# -----------------------
with st.form("study_form"):
    subject = st.text_input("과목명 또는 학습 활동")
    hours = st.number_input("투자한 시간 (시간)", min_value=0.0, step=0.5)
    satisfaction = st.slider("학습 만족도 (0~100)", 0, 100, 70)
    achievement = st.slider("목표 달성률 (0~100)", 0, 100, 60)
    submitted = st.form_submit_button("기록하기")

# -----------------------
# 데이터 저장 (Session 상태 사용)
# -----------------------
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["과목", "시간", "만족도", "달성률"])

if submitted:
    new_data = pd.DataFrame([[subject, hours, satisfaction, achievement]],
                            columns=["과목", "시간", "만족도", "달성률"])
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)

# -----------------------
# 데이터 시각화
# -----------------------
if not st.session_state.data.empty:
    st.subheader("📊 학습 시간 분포")
    fig1 = px.pie(st.session_state.data, names="과목", values="시간", title="과목별 학습 시간")
    st.plotly_chart(fig1)

    st.subheader("📈 목표 달성률 비교")
    fig2 = px.bar(st.session_state.data, x="과목", y="달성률", color="과목", title="과목별 목표 달성률")
    st.plotly_chart(fig2)

    st.subheader("🔍 학습 피드백")
    for idx, row in st.session_state.data.iterrows():
        if row["만족도"] < 50:
            st.warning(f"{row['과목']}의 만족도가 낮습니다. 학습 방식 점검이 필요합니다.")
        elif row["달성률"] < 50:
            st.info(f"{row['과목']}의 목표 달성률이 낮습니다. 계획 조정이 필요할 수 있습니다.")
        else:
            st.success(f"{row['과목']}은(는) 잘 진행되고 있습니다! 계속 유지하세요.")

# -----------------------
# 데이터 확인
# -----------------------
st.subheader("📋 전체 학습 기록")
st.dataframe(st.session_state.data)
