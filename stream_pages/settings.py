import streamlit as st

# =============================================================
# 환경 설정 페이지 (Settings)
# =============================================================

st.title("⚙️ Settings")
st.caption("공식 문서의 Settings 페이지 예시입니다. 환경 설정을 관리하고 페이지 전환을 체험합니다.")

# [로그인 보호] 로그인하지 않은 사용자는 접근 차단
if not st.user.get("is_logged_in", False):
    st.warning("🔒 로그인이 필요한 페이지입니다. 먼저 로그인해 주세요.")
    st.page_link("login.py", label="로그인 페이지로 이동", icon=":material/login:")
    st.stop()



st.subheader("🛠️ 일반 환경 설정")

# 1. 토글 스위치 (st.toggle)
dark_mode = st.toggle("🌙 다크 모드 활성화", value=False)
if dark_mode:
    st.info("다크 모드가 활성화되었습니다.")

# 2. 언어 선택 상자 (st.selectbox)
language = st.selectbox(
    "🌐 기본 언어 선택",
    options=["한국어", "English", "日本語", "Español"]
)
st.write(f"선택된 언어: **{language}**")

# 3. 알림 수신 주기 슬라이더 (st.slider)
alert_freq = st.slider("🔔 일일 알림 최대 횟수", min_value=1, max_value=10, value=3)
st.write(f"설정된 알림: 하루 최대 **{alert_freq}회**")

st.divider()

# 4. 코드로 다른 페이지 즉시 전환 (st.switch_page)
st.subheader("🔄 코드로 페이지 즉시 전환 (st.switch_page)")
st.markdown("버튼을 누르면 파이썬 코드가 실행되면서 대시보드 페이지로 즉시 화면이 전환됩니다.")

if st.button("📊 대시보드 페이지로 즉시 전환하기", type="primary"):
    st.switch_page("dashboard.py")

