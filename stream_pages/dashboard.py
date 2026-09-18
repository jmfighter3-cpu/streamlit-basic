import streamlit as st
import pandas as pd

# =============================================================
# 서비스 대시보드 페이지 (Service Dashboard)
# =============================================================

st.title("📈 Overview")
st.caption("공식 문서의 Reports > Overview 페이지 예시입니다. 서비스 핵심 지표와 차트를 제공합니다.")

# [로그인 보호] 로그인하지 않은 사용자는 접근 차단
if not st.user.get("is_logged_in", False):
    st.warning("🔒 로그인이 필요한 페이지입니다. 먼저 로그인해 주세요.")
    st.page_link("login.py", label="로그인 페이지로 이동", icon=":material/login:")
    st.stop()



# 1. 주요 핵심 지표 (st.metric)
# - label: 지표 이름
# - value: 현재 수치
# - delta: 이전 대비 변동치
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="총 사용자 수", value="1,240명", delta="+12%")
with col2:
    st.metric(label="일일 방문자", value="350명", delta="+5%")
with col3:
    st.metric(label="전환율", value="4.8%", delta="-0.2%")

st.divider()

# 2. 간단한 주간 추이 차트 (st.line_chart)
st.subheader("📈 주간 방문자 추이")

# 간단한 샘플 데이터 생성
chart_data = pd.DataFrame({
    "방문자 수": [120, 150, 180, 220, 310, 280, 350]
}, index=["월", "화", "수", "목", "금", "토", "일"])

st.line_chart(chart_data)

st.divider()

# 3. 다른 페이지 바로가기 링크 (st.page_link 실전 활용)
st.divider()
st.caption("🧭 빠른 메뉴 바로가기 (st.page_link)")
col_link1, col_link2 = st.columns(2)
with col_link1:
    st.page_link("settings.py", label="환경설정 변경하기", icon=":material/settings:")
with col_link2:
    st.page_link("logout.py", label="로그아웃 페이지로 이동", icon=":material/logout:")


