import os
import streamlit as st
from dotenv import load_dotenv

# 1. .env 파일에서 환경 변수 불러오기
load_dotenv()

# 2. .env 환경 변수를 바탕으로 Streamlit 인증 secrets 구성
# secrets.toml 대신 .env 에 정의된 변수들을 st.App 에 직접 주입합니다.
auth_secrets = {
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
}

# 3. st.App 생성 시 secrets 전달 (공식 지원 기능)
app = st.App(r"stream_pages\main.py", secrets=auth_secrets)

if __name__ == '__main__':
    app.run()
