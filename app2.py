import streamlit as st
import os
import base64
import sqlite3
from datetime import datetime
import uuid
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
    /* Streamlit 기본 사이드바 네비게이션(상단 파일명 목록 및 구분선) 숨기기 */
    [data-testid="stSidebarNav"] {
        display: none !important;
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
# 1. 환경변수(.env) 로드 (로컬 개발 편의용)
# =============================================================
load_dotenv()
env_api_key = os.getenv("OPENAI_API_KEY")

# .env에 공백이 포함된 경우도 유연하게 지원
if not env_api_key and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "=" in line and ("OPENAI" in line.upper() and "KEY" in line.upper()):
                env_api_key = line.split("=", 1)[1].strip()
                break

# =============================================================
# 2. SQLite 데이터베이스 설정 및 세션/대화 관리 함수
# =============================================================
DB_PATH = "chat_history.db"

def init_db():
    """SQLite 데이터베이스 테이블(세션 및 메시지)을 초기화하고 마이그레이션합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1) 세션 테이블 (최대 10개 세션 보관)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            session_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            turn_count INTEGER DEFAULT 0
        )
    """)
    
    # 2) 메시지 테이블 (세션별 최대 100턴 = 200개 메시지 보관)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL DEFAULT 'default_session',
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            has_image INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 기존 DB 스키마에 session_id 컬럼이 없을 경우 자동 추가
    cursor.execute("PRAGMA table_info(chat_messages)")
    columns = [col[1] for col in cursor.fetchall()]
    if "session_id" not in columns:
        cursor.execute("ALTER TABLE chat_messages ADD COLUMN session_id TEXT DEFAULT 'default_session'")
        
    conn.commit()
    conn.close()

def cleanup_old_sessions():
    """최대 10개의 세션만 유지하며, 10개를 초과하면 가장 오래된 세션부터 자동 영구 삭제(FIFO)합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM chat_sessions ORDER BY updated_at DESC")
    sessions = cursor.fetchall()
    
    # 10개를 초과하는 오래된 세션 삭제
    if len(sessions) > 10:
        old_sessions = sessions[10:]
        old_ids = [s[0] for s in old_sessions]
        placeholders = ",".join("?" * len(old_ids))
        cursor.execute(f"DELETE FROM chat_messages WHERE session_id IN ({placeholders})", old_ids)
        cursor.execute(f"DELETE FROM chat_sessions WHERE session_id IN ({placeholders})", old_ids)
        conn.commit()
        
    conn.close()

def create_new_session(title="새로운 대화"):
    """새로운 대화 세션을 생성하고 고유 session_id를 반환합니다."""
    session_id = f"sess_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_sessions (session_id, title, turn_count) VALUES (?, ?, 0)",
        (session_id, title)
    )
    conn.commit()
    conn.close()
    
    # 10개 세션 초과 시 자동 FIFO 정리
    cleanup_old_sessions()
    return session_id

def get_sessions():
    """최근 업데이트된 세션 목록(최대 10개)을 반환합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, turn_count, updated_at FROM chat_sessions ORDER BY updated_at DESC LIMIT 10")
    sessions = cursor.fetchall()
    conn.close()
    return sessions

def load_session_messages(session_id):
    """특정 세션의 대화 내역을 불러옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT role, content, has_image FROM chat_messages WHERE session_id = ? ORDER BY id ASC",
        (session_id,)
    )
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

def save_message_to_db(session_id, role, content, has_image=False):
    """메시지를 저장하고, 세션 내 100회(200개 메시지) 초과 시 가장 오래된 메시지부터 롤링 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. 세션 존재 여부 확인 및 제목 갱신
    cursor.execute("SELECT session_id, title FROM chat_sessions WHERE session_id = ?", (session_id,))
    sess = cursor.fetchone()
    if not sess:
        clean_title = content[:20] + "..." if len(content) > 20 else content
        cursor.execute(
            "INSERT INTO chat_sessions (session_id, title, turn_count) VALUES (?, ?, 0)",
            (session_id, clean_title)
        )
    elif sess[1] in ("새로운 대화", "기존 대화 세션") and role == "user":
        clean_title = content[:20] + "..." if len(content) > 20 else content
        cursor.execute("UPDATE chat_sessions SET title = ? WHERE session_id = ?", (clean_title, session_id))

    # 2. 메시지 삽입
    cursor.execute(
        "INSERT INTO chat_messages (session_id, role, content, has_image) VALUES (?, ?, ?, ?)",
        (session_id, role, content, 1 if has_image else 0)
    )
    
    # 3. 세션당 최대 100회 대화 제한 (1회 = 질문+답변 = 2개 메시지 -> 최대 200개 메시지)
    cursor.execute("SELECT id FROM chat_messages WHERE session_id = ? ORDER BY id ASC", (session_id,))
    msg_ids = [row[0] for row in cursor.fetchall()]
    if len(msg_ids) > 200:
        excess = len(msg_ids) - 200
        delete_ids = msg_ids[:excess]
        placeholders = ",".join("?" * len(delete_ids))
        cursor.execute(f"DELETE FROM chat_messages WHERE id IN ({placeholders})", delete_ids)

    # 4. 세션 갱신 시각 및 대화 턴 수 업데이트
    current_turns = min(len(msg_ids) // 2, 100)
    cursor.execute(
        "UPDATE chat_sessions SET updated_at = CURRENT_TIMESTAMP, turn_count = ? WHERE session_id = ?",
        (current_turns, session_id)
    )
    conn.commit()
    conn.close()

def delete_session(session_id):
    """특정 세션과 해당 대화 내역을 영구 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

# DB 초기화 실행
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
if "user_api_key" not in st.session_state:
    st.session_state.user_api_key = ""

if "current_session_id" not in st.session_state:
    existing = get_sessions()
    if existing:
        st.session_state.current_session_id = existing[0][0]
    else:
        st.session_state.current_session_id = create_new_session("새로운 대화")

if "messages" not in st.session_state:
    loaded = load_session_messages(st.session_state.current_session_id)
    if loaded:
        st.session_state.messages = loaded
    else:
        st.session_state.messages = [
            {"role": "assistant", "content": "안녕하세요! AI Studio 챗봇입니다. 질문을 입력하거나 이미지를 첨부해 보세요!"}
        ]

if "attached_image" not in st.session_state:
    st.session_state.attached_image = None
if "attached_file" not in st.session_state:
    st.session_state.attached_file = None

# =============================================================
# 5. 배포 환경 키 등록 게이트 (키 미등록 시 동작 차단)
# =============================================================
if not st.session_state.user_api_key:
    # 사이드바: 미인증 안내
    with st.sidebar:
        st.markdown("### ✨ AI Studio")
        st.caption("멀티모달 챗봇 & 대화 관리 시스템")
        st.divider()
        st.markdown("#### 🔒 인증 필요")
        st.info("AI 채팅을 시작하려면 우측 화면에서 본인의 OpenAI API 키를 먼저 등록해 주세요.")

    # 메인 로그인/키 등록 카드
    st.markdown("## 🔐 AI Studio 로그인 및 API Key 등록")
    st.caption("배포된 웹 환경에서 안전하게 챗봇을 이용하기 위해 API 키를 등록합니다.")
    
    with st.container(border=True):
        st.markdown("### 🔑 OpenAI API Key 등록")
        st.write("본인의 OpenAI API 키(`sk-...`)를 입력하고 등록을 완료하면 AI 채팅이 활성화됩니다.")
        
        # 보안 취약점 안내 메시지 (로그인 페이지)
        st.warning("""
        🛡️ **보안 취약성 및 API 키 보호 안내 (필독)**
        - **키 보관 원칙**: 입력하신 API 키는 **브라우저 세션 메모리(`st.session_state`)에만 임시 보관**되며, 서버나 데이터베이스에 절대 영구 저장되지 않습니다.
        - **공용 환경 주의**: 학교, 카페, 공용 PC 등 타인과 공유하는 환경에서는 이용 후 사이드바의 **'🔓 로그아웃 / 키 해제'** 버튼을 반드시 눌러 키를 삭제해 주세요.
        - **과금 방지**: 유출 시 무단 과금 피해가 발생할 수 있으므로, [OpenAI 대시보드](https://platform.openai.com/account/limits)에서 월별 사용 한도(Usage limits)를 설정해 두는 것을 강력히 권장합니다.
        """)
        
        input_key = st.text_input(
            label="OpenAI API 키 입력",
            type="password",
            placeholder="sk-proj-...",
            help="OpenAI 플랫폼에서 발급받은 비밀 키(sk-...)를 입력하세요."
        )
        
        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            if st.button("🚀 키 등록하고 AI 채팅 시작", type="primary", use_container_width=True):
                clean_key = input_key.strip()
                if clean_key.startswith("sk-") and len(clean_key) > 20:
                    st.session_state.user_api_key = clean_key
                    st.success("API 키가 성공적으로 등록되었습니다!")
                    st.rerun()
                else:
                    st.error("올바른 형식의 OpenAI API 키(sk-...)를 입력해 주세요.")
                    
        with col_btn2:
            # 로컬에 .env 키가 있는 경우 개발 편의 버튼 제공
            if env_api_key:
                if st.button("⚡ .env 키로 빠른 시작", use_container_width=True, help="로컬 환경변수에 저장된 키를 사용합니다."):
                    st.session_state.user_api_key = env_api_key
                    st.rerun()

    st.stop()  # 키가 등록되기 전까지 아래 채팅 로직의 실행을 안전하게 차단합니다!

# =============================================================
# 6. 사이드바: 네비게이션, 세션 관리 및 모델 설정
# =============================================================
with st.sidebar:
    # 1. 일관된 브랜드 헤더 및 네비게이션 메뉴 (최상단)
    st.markdown("### ✨ AI Studio")
    st.caption("멀티모달 챗봇 & 대화 관리 시스템")
    
    st.markdown("#### 🧭 메뉴")
    st.page_link("app2.py", label="AI 채팅 (Chat)", icon="💬")
    st.page_link("pages/app2_history.py", label="대화 내역 보관함 (History)", icon="📜")
    
    st.divider()

    # 2. 인증 상태 및 로그아웃
    st.markdown("#### 🔐 보안 및 인증")
    st.success("API 키 활성화됨", icon="🔑")
    if st.button("🔓 로그아웃 / 키 해제", use_container_width=True, help="등록된 API 키를 비우고 세션을 안전하게 종료합니다."):
        st.session_state.user_api_key = ""
        st.session_state.messages = []
        st.session_state.attached_image = None
        st.session_state.attached_file = None
        st.rerun()

    st.divider()

    # 3. 대화 세션 관리 (최대 10개)
    st.markdown("#### 📂 대화 세션 (최대 10개)")
    if st.button("➕ 새 대화 시작", type="primary", use_container_width=True):
        new_sid = create_new_session("새로운 대화")
        st.session_state.current_session_id = new_sid
        st.session_state.messages = [
            {"role": "assistant", "content": "새로운 대화 세션이 시작되었습니다. 질문을 입력해 주세요!"}
        ]
        st.session_state.attached_image = None
        st.session_state.attached_file = None
        st.rerun()
        
    all_sessions = get_sessions()
    session_options = [s[0] for s in all_sessions]
    session_titles = {s[0]: f"{s[1]} ({s[2]}/100회)" for s in all_sessions}
    
    # 현재 세션이 목록에 없으면 첫 번째 세션으로 보정
    if st.session_state.current_session_id not in session_options and session_options:
        st.session_state.current_session_id = session_options[0]
        
    if session_options:
        curr_idx = session_options.index(st.session_state.current_session_id) if st.session_state.current_session_id in session_options else 0
        selected_sid = st.selectbox(
            label="세션 목록 선택",
            options=session_options,
            index=curr_idx,
            format_func=lambda sid: session_titles.get(sid, sid),
            help="원하는 대화 세션을 선택해 이전 대화를 이어갈 수 있습니다."
        )
        
        if selected_sid != st.session_state.current_session_id:
            st.session_state.current_session_id = selected_sid
            loaded = load_session_messages(selected_sid)
            st.session_state.messages = loaded if loaded else [
                {"role": "assistant", "content": "대화 세션을 불러왔습니다. 질문을 입력해 주세요!"}
            ]
            st.session_state.attached_image = None
            st.session_state.attached_file = None
            st.rerun()

    st.divider()

    # 4. 모델 선택
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

# =============================================================
# 7. 메인 채팅 화면 및 정돈된 툴바
# =============================================================
# 현재 세션 제목 및 턴 수 계산
curr_title = session_titles.get(st.session_state.current_session_id, "대화 세션")
user_turn_count = len([m for m in st.session_state.messages if m["role"] == "user"])

st.markdown("## 💬 AI Studio Multimodal Chat")
st.caption(f"엔진: **:blue[{selected_model}]** · 세션: **{curr_title}**")

# 보안 취약점 안내 메시지 (채팅 기능)
with st.expander("🔒 **개인정보 및 기밀 데이터 보안 수칙 (필독)**", expanded=False):
    st.markdown("""
    - **데이터 전송 주의**: 대화 내용 및 첨부 파일(이미지, 문서)은 AI 답변 생성을 위해 OpenAI 서버로 암호화 전송됩니다.
    - **민감 정보 입력 금지**: 주민등록번호, 계좌번호, 비밀번호, 사내 기밀 등 민감한 개인정보나 대외비 문서는 절대 입력하지 마세요.
    - **자동 보관 정책**: 한 세션당 최대 **100회(턴)**까지 보관되며, 초과 시 가장 오래된 대화부터 자동 순환(롤링)됩니다.
    """)

# 첨부 액션 툴바 및 진행 상태 (Streamlit container 활용)
with st.container(border=True):
    col_tool1, col_tool2, col_turn = st.columns([1.2, 1.2, 2.6])
    
    with col_tool1:
        if st.button("📷 이미지 첨부", use_container_width=True):
            upload_image_dialog()
            
    with col_tool2:
        if st.button("📄 문서 첨부", use_container_width=True):
            upload_doc_dialog()
            
    with col_turn:
        st.caption(f"📊 세션 대화 진행: **{user_turn_count} / 100회** (질문+답변=1회)")

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
# 8. 대화 내역 렌더링 (커스텀 아바타 적용)
# =============================================================
for msg in st.session_state.messages:
    avatar_icon = "👤" if msg["role"] == "user" else "✨"
    with st.chat_message(msg["role"], avatar=avatar_icon):
        st.markdown(msg["content"])
        if "image_bytes" in msg:
            st.image(msg["image_bytes"], width=280)

# =============================================================
# 9. 사용자 채팅 입력 및 응답 생성
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

    # 2) 세션 및 SQLite DB에 사용자 메시지 저장
    user_record = {"role": "user", "content": user_prompt}
    if attached_img_bytes:
        user_record["image_bytes"] = attached_img_bytes
    st.session_state.messages.append(user_record)
    save_message_to_db(st.session_state.current_session_id, "user", user_prompt, has_image=has_img)

    # 3) OpenAI API 호출용 페이로드 조립
    openai_client = OpenAI(api_key=st.session_state.user_api_key)

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

    # 5) AI 답변 세션 및 SQLite DB 저장 (턴 수 갱신 및 100회 한도 롤링 적용)
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    save_message_to_db(st.session_state.current_session_id, "assistant", response_text, has_image=False)

    # 6) 첨부 상태 초기화 후 새로고침
    st.session_state.attached_image = None
    st.session_state.attached_file = None
    st.rerun()
