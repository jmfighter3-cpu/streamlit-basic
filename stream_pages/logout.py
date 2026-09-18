import streamlit as st

# =============================================================
# 로그아웃 전용 페이지 (Log out)
# 공식 문서: https://docs.streamlit.io/develop/api-reference/user/st.logout
# =============================================================

st.title("🚪 Log out")
st.caption("Streamlit 공식 st.logout() API를 실행하는 전용 로그아웃 페이지입니다.")

# 로그인 여부 확인
is_logged_in = st.user.get("is_logged_in", False)

if is_logged_in:
    user_name = st.user.get("name") or st.user.get("email") or "사용자"
    st.info(f"현재 **{user_name}** 계정으로 로그인되어 있습니다.")

    st.markdown("아래 버튼을 누르면 세션 쿠키가 삭제되고 로그아웃됩니다.")

    col_o1, col_o2 = st.columns([1, 1])
    with col_o1:
        # 공식 st.logout() 호출 버튼
        if st.button("🔴 로그아웃 실행", icon=":material/logout:", type="primary"):
            st.logout()
    with col_o2:
        st.page_link("dashboard.py", label="취소하고 Overview로 가기", icon=":material/arrow_back:")

else:
    st.success("현재 안전하게 로그아웃된 상태입니다.")
    st.page_link("login.py", label="로그인 페이지로 이동", icon=":material/login:")

