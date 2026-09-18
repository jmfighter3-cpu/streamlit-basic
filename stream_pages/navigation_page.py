import streamlit as st

# =============================================================
# Streamlit 공식 Navigation and pages 종합 쇼케이스
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation
# =============================================================

st.title("🧭 Navigation and pages")
st.caption("공식 API 레퍼런스의 4대 핵심 기능(Navigation, Page, Page link, Switch page)을 한눈에 둘러보고 체험합니다.")

st.divider()

# 상단 2개 카드 (Navigation & Page)
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("📌 Navigation (`st.navigation`)")
        st.caption("Configure the available pages in a multipage app.")
        st.code('''pg = st.navigation({
    "Your Account": [page_login],
    "Reports": [page_dashboard],
    "Tools": [page_settings],
    "Navigation": [page_nav_demo]
})
pg.run()''', language="python")
        st.info("👈 **좌측 사이드바**를 확인해 보세요! 공식 문서와 동일한 섹션 구조로 메뉴가 작동하고 있습니다.")

with col2:
    with st.container(border=True):
        st.subheader("📄 Page (`st.Page`)")
        st.caption("Define a page in a multipage app.")
        st.code('''home = st.Page(
    "login.py",
    title="로그인 / 내 계정",
    icon=":material/account_circle:",
    default=True
)''', language="python")
        st.success("✅ 파일 경로, 아이콘(Material Symbols), 메뉴 타이틀을 지정하여 페이지 객체를 생성합니다.")

# 하단 2개 카드 (Page link & Switch page)
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.subheader("🔗 Page link (`st.page_link`)")
        st.caption("Display a link to another page in a multipage app.")
        st.code('''st.page_link("login.py", label="Home", icon=":material/home:")
st.page_link("dashboard.py", label="Dashboard", icon=":material/monitoring:")
st.page_link("https://docs.streamlit.io", label="Streamlit Docs", icon=":material/public:")''', language="python")
        st.markdown("**👇 직접 클릭해 보세요:**")
        st.page_link("login.py", label="Home (로그인 페이지로 이동)", icon=":material/home:")
        st.page_link("dashboard.py", label="Dashboard (대시보드로 이동)", icon=":material/monitoring:")
        st.page_link("https://docs.streamlit.io", label="Streamlit 공식 문서 (외부 링크)", icon=":material/public:")

with col4:
    with st.container(border=True):
        st.subheader("🔄 Switch page (`st.switch_page`)")
        st.caption("Programmatically navigates to a specified page.")
        st.code('''if st.button("대시보드로 즉시 이동"):
    st.switch_page("dashboard.py")''', language="python")
        st.markdown("**👇 직접 버튼을 눌러보세요:**")
        if st.button("대시보드로 즉시 전환하기", icon=":material/arrow_forward:", type="primary"):
            st.switch_page("dashboard.py")
