import streamlit as st
import os
import base64
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI

# =============================================================
# 0. 페이지 기본 설정 및 모던 미감 스타일링
# =============================================================
st.set_page_config(
    page_title="AI Studio Assistant",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 모던 미니멀 UI 커스텀 CSS (부드러운 모서리, 여백, 호버 인터랙션)
st.markdown("""
<style>
    /* 전체 상단 패딩 조절 */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }
    /* 버튼 둥근 모서리 및 부드러운 그림자 효과 */
    .stButton > button {
        border-radius: 12px;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }
    /* 상태 안내 카드 둥글기 */
    div[data-testid="stNotification"] {
        border-radius: 12px;
    }
    /* 비밀번호 입력창의 눈 아이콘(보기/숨기기 토글 버튼) 완전 제거 */
    div[data-testid="stTextInputRootElement"] button:not([data-testid="stTextInputClearButton"]),
    div[data-testid="stTextInputRootElement"] button[aria-label*="password" i],
    div[data-testid="stTextInputRootElement"] button[aria-label*="Password"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================
# 1. 환경변수(.env) 로드 및 OpenAI API 키 읽기
# =============================================================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# .env에 공백이 포함된 경우도 유연하게 지원
if not api_key and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and ("OPENAI" in line.upper() and "KEY" in line.upper()):
                api_key = line.split("=", 1)[1].strip()
                break

# =============================================================
# 2. SQLite 데이터베이스 설정 및 헬퍼 함수
# =============================================================
DB_PATH = "chat_history.db"

def init_db():
    """SQLite 데이터베이스 및 채팅 내역 테이블을 생성합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            has_image INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def get_message_count():
    """SQLite DB에 저장된 총 메시지 개수를 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM chat_messages")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def load_chat_history():
    """SQLite DB에서 이전 대화 기록을 모두 불러옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT role, content, has_image FROM chat_messages ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    
    messages = []
    for role, content, has_image in rows:
        messages.append({
            "role": role,
            "content": content,
            "has_image": bool(has_image)
        })
    return messages

def save_message(role, content, has_image=False):
    """새로운 메시지를 SQLite DB에 저장합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_messages (role, content, has_image) VALUES (?, ?, ?)",
        (role, content, 1 if has_image else 0)
    )
    conn.commit()
    conn.close()

def clear_chat_history():
    """SQLite DB의 모든 대화 기록을 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages")
    conn.commit()
    conn.close()

# DB 테이블 초기화
init_db()

# =============================================================
# 3. 팝업창(모달 다이얼로그) 정의
# =============================================================
@st.dialog("📷 이미지 업로드")
def upload_image_dialog():
    st.write("이미지 파일을 아래 영역으로 **드래그 앤 드롭**하세요.")
    img_file = st.file_uploader(
        label="이미지 파일 선택",
        type=["png", "jpg", "jpeg", "webp"],
        key="popup_image_uploader"
    )
    if img_file:
        st.image(img_file, caption=f"선택됨: {img_file.name}", width=250)
        if st.button("✨ 이 이미지 첨부하기", type="primary", use_container_width=True):
            st.session_state.attached_image = img_file
            st.rerun()

@st.dialog("📄 문서 파일 업로드")
def upload_doc_dialog():
    st.write("텍스트 또는 데이터 파일을 아래 영역으로 **드래그 앤 드롭**하세요.")
    doc_file = st.file_uploader(
        label="문서 파일 선택",
        type=["txt", "csv", "md", "json"],
        key="popup_doc_uploader"
    )
    if doc_file:
        st.write(f"선택된 파일: **{doc_file.name}**")
        if st.button("✨ 이 파일 첨부하기", type="primary", use_container_width=True):
            st.session_state.attached_file = doc_file
            st.rerun()

# =============================================================
# 4. 세션 상태 초기화
# =============================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 무엇이든 물어보세요. 이미지나 파일을 첨부하여 질문하실 수도 있습니다."}
    ]

if "attached_image" not in st.session_state:
    st.session_state.attached_image = None

if "attached_file" not in st.session_state:
    st.session_state.attached_file = None

# =============================================================
# 5. 사이드바: 모델 설정 및 이전 대화 관리
# =============================================================
with st.sidebar:
    # 1. 일관된 브랜드 헤더 및 네비게이션 메뉴 (최상단)
    st.markdown("### ✨ AI Studio")
    st.caption("멀티모달 챗봇 & 대화 관리 시스템")
    
    st.markdown("#### 🧭 메뉴")
    st.page_link("app2.py", label="💬 AI 채팅 (Chat)", icon="💬")
    st.page_link("pages/app2_history.py", label="📜 대화 내역 보관함 (History)", icon="📜")
    
    st.divider()

    # 2. 채팅 환경 설정
    st.markdown("#### ⚙️ 채팅 환경 설정")
    if api_key:
        st.success("API 키 자동 연동됨 (.env)", icon="🔑")
    else:
        st.warning("API 키를 입력해주세요", icon="⚠️")

    # API 키 입력창: 눈 아이콘은 CSS로 제거되며, .env에 키가 있으면 원본 키를 value에 노출하지 않아 브라우저 유출을 방지
    api_key_input = st.text_input(
        label="OpenAI API 키",
        value="",
        placeholder="•••••••••••••••• (환경변수 .env 키 적용 중)" if api_key else "sk-proj-...",
        type="password",
        help="OpenAI API 키를 직접 입력하거나 .env 파일에 등록해 두세요."
    )

    # 모델 선택
    st.markdown("#### 🤖 모델 엔진 선택")
    available_models = [
        "gpt-5.6-luna",   # ⚡ 빠르고 경제적인 경량 모델 (기본값)
        "gpt-5.6-terra",  # ⚖️ 성능과 비용의 균형 모델
        "gpt-5.6-sol",    # 🧠 코딩 및 심층 분석용 최고 플래그십
        "gpt-5.5"         # 🏛️ 범용 기본 모델
    ]

    selected_model = st.selectbox(
        label="사용할 모델",
        options=available_models,
        index=0
    )
    model_descriptions = {
        "gpt-5.6-luna": "⚡ 고속·고효율 경량 모델 (기본 추천)",
        "gpt-5.6-terra": "⚖️ 지능과 경제성의 균형 모델",
        "gpt-5.6-sol": "🧠 복잡한 코딩·과학 분석용 최고 플래그십",
        "gpt-5.5": "🏛️ 범용 기본 모델"
    }
    st.caption(model_descriptions.get(selected_model, ""))

    st.divider()

    # 3. 대화 내역 관리 섹션
    st.markdown("#### 💾 대화 관리 (SQLite)")
    saved_count = get_message_count()
    st.caption(f"DB에 저장된 메시지: **{saved_count}개**")

    col_h1, col_h2 = st.columns(2)
    with col_h1:
        if st.button("📥 불러오기", use_container_width=True, help="SQLite DB에서 이전 대화 복원"):
            history = load_chat_history()
            if history:
                st.session_state.messages = history
                st.rerun()
    with col_h2:
        if st.button("🗑️ 초기화", use_container_width=True, help="DB와 화면 대화 내역 모두 비우기"):
            clear_chat_history()
            st.session_state.messages = [
                {"role": "assistant", "content": "대화 내역이 초기화되었습니다. 새로운 질문을 입력해 주세요!"}
            ]
            st.session_state.attached_image = None
            st.session_state.attached_file = None
            st.rerun()

# =============================================================
# 6. 메인 채팅 화면 및 정돈된 툴바
# =============================================================
st.markdown("## 💬 AI Studio Multimodal Chat")
st.caption(f"엔진: **:blue[{selected_model}]** · 질문에 이미지나 문서 파일을 첨부해 분석해 보세요.")

# 첨부 액션 툴바
col_tool1, col_tool2, col_tool_info = st.columns([1.2, 1.2, 2.6])

with col_tool1:
    if st.button("📷 이미지 첨부", use_container_width=True):
        upload_image_dialog()

with col_tool2:
    if st.button("📄 문서 첨부", use_container_width=True):
        upload_doc_dialog()

with col_tool_info:
    # 첨부된 상태를 우측에 컴팩트하게 배지 형태로 알림
    if st.session_state.attached_image or st.session_state.attached_file:
        st.info("📌 전송 대기 중인 파일이 있습니다.", icon="📎")

# 현재 첨부 대기 중인 항목 카드 표시
if st.session_state.attached_image or st.session_state.attached_file:
    with st.container(border=True):
        st.markdown("##### 📎 첨부 대기 항목")
        col_preview1, col_preview2 = st.columns(2)
        
        with col_preview1:
            if st.session_state.attached_image:
                st.image(st.session_state.attached_image, caption=f"📷 {st.session_state.attached_image.name}", width=160)
                if st.button("❌ 이미지 제외", key="btn_remove_img"):
                    st.session_state.attached_image = None
                    st.rerun()
                    
        with col_preview2:
            if st.session_state.attached_file:
                st.write(f"📄 **{st.session_state.attached_file.name}**")
                file_size_kb = len(st.session_state.attached_file.getvalue()) / 1024
                st.caption(f"파일 크기: {file_size_kb:.1f} KB")
                if st.button("❌ 파일 제외", key="btn_remove_file"):
                    st.session_state.attached_file = None
                    st.rerun()

st.divider()

# =============================================================
# 7. 대화 내역 렌더링 (커스텀 아바타 적용)
# =============================================================
for msg in st.session_state.messages:
    avatar_icon = "👤" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        if "image_bytes" in msg:
            st.image(msg["image_bytes"], width=280)

# =============================================================
# 8. 사용자 채팅 입력 및 응답 생성
# =============================================================
user_prompt = st.chat_input("메시지를 입력하세요...")

if user_prompt:
    # 1) 사용자 메시지 화면 출력 (아바타 지정)
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_prompt)
        cur_img = st.session_state.attached_image
        cur_file = st.session_state.attached_file
        
        attached_img_bytes = None
        has_img = False
        if cur_img:
            attached_img_bytes = cur_img.getvalue()
            has_img = True
            st.image(attached_img_bytes, width=280)
        if cur_file:
            st.caption(f"📎 첨부 파일: {cur_file.name}")

    # 2) 세션 및 SQLite DB에 저장
    user_record = {"role": "user", "content": user_prompt}
    if attached_img_bytes:
        user_record["image_bytes"] = attached_img_bytes
    st.session_state.messages.append(user_record)
    save_message("user", user_prompt, has_image=has_img)

    # 3) OpenAI API 호출용 페이로드 조립
    active_key = api_key_input if api_key_input else api_key
    openai_client = OpenAI(api_key=active_key)

    user_content = [{"type": "text", "text": user_prompt}]

    if cur_img:
        base64_img = base64.b64encode(cur_img.getvalue()).decode("utf-8")
        user_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{cur_img.type};base64,{base64_img}"}
        })
    if cur_file:
        file_text = cur_file.getvalue().decode("utf-8", errors="ignore")
        user_content.append({
            "type": "text",
            "text": f"\n\n[사용자 첨부 파일({cur_file.name}) 내용]:\n{file_text}"
        })

    api_messages = []
    for msg in st.session_state.messages[:-1]:
        api_messages.append({"role": msg["role"], "content": msg["content"]})
    api_messages.append({"role": "user", "content": user_content})

    # 4) OpenAI 모델 응답 스트리밍 출력 (아바타 지정)
    with st.chat_message("assistant", avatar="✨"):
        response_stream = openai_client.chat.completions.create(
            model=selected_model,
            messages=api_messages,
            stream=True
        )
        response_text = st.write_stream(response_stream)

    # 5) AI 답변 세션 및 SQLite DB 저장
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    save_message("assistant", response_text, has_image=False)

    # 6) 첨부 상태 초기화 후 새로고침
    st.session_state.attached_image = None
    st.session_state.attached_file = None
    st.rerun()
