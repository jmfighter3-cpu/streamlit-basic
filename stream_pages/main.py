import os
import streamlit as st
from dotenv import load_dotenv
from streamlit.runtime.secrets import secrets_singleton

# .env 환경 변수 불러오기 및 Streamlit secrets 주입
load_dotenv()

if os.getenv("GOOGLE_CLIENT_ID"):
    secrets_singleton.merge_programmatic_secrets({
        "auth": {
            "redirect_uri": os.getenv("AUTH_REDIRECT_URI", "http://localhost:8501/oauth2callback"),
            "cookie_secret": os.getenv("AUTH_COOKIE_SECRET", "super-secret-cookie-key-for-google-auth"),
            "google": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET", ""),
                "server_metadata_url": os.getenv(
                    "GOOGLE_SERVER_METADATA_URL",
                    "https://accounts.google.com/.well-known/openid-configuration"
                ),
            }
        }
    })

# =============================================================
# Streamlit 공식 네비게이션 총괄 라우터 (Entrypoint)
# 공식 문서: https://docs.streamlit.io/develop/api-reference/navigation
# =============================================================

# 1. 로그인 여부 확인
is_logged_in = st.user.get("is_logged_in", False)

# 2. st.Page 로 각 서브 페이지 정의 (공식 문서와 100% 동일한 명칭 및 아이콘)
# - 미로그인 시: Log in 페이지가 기본(default=True)으로 열립니다.
# - 로그인 완료 시: Overview(대시보드) 페이지가 기본(default=True)으로 열립니다!
page_login = st.Page(
    "login.py",
    title="Log in",
    icon=":material/login:",
    default=(not is_logged_in)
)

page_logout = st.Page(
    "logout.py",
    title="Log out",
    icon=":material/logout:"
)

page_settings = st.Page(
    "settings.py",
    title="Settings",
    icon=":material/settings:"
)

page_overview = st.Page(
    "dashboard.py",
    title="Overview",
    icon=":material/monitoring:",
    default=is_logged_in
)

page_nav_demo = st.Page(
    "navigation_page.py",
    title="Navigation and pages",
    icon=":material/explore:"
)

# 3. 공식 문서 이미지 구조 완벽 매칭:
# - "Your account": 로그인 시 [Log out, Settings] / 미로그인 시 [Log in, Settings]
# - "Reports": [Overview]
# - "Navigation": [Navigation and pages]
account_pages = [page_logout, page_settings] if is_logged_in else [page_login, page_settings]

pg = st.navigation({
    "Your account": account_pages,
    "Reports": [page_overview],
    "Navigation": [page_nav_demo]
})

# 4. 사이드바 하단 상태 표시
with st.sidebar:
    st.divider()
    if is_logged_in:
        user_name = st.user.get("name") or st.user.get("email") or "사용자"
        st.success(f"🟢 **{user_name}**")
    else:
        st.caption("⚪ 로그인되지 않음")

# 5. 사용자가 선택한 페이지 실행
pg.run()



