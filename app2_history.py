import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import uuid

# =============================================================
# 0. 페이지 설정 및 모던 미니멀 스타일링
# =============================================================
st.set_page_config(
    page_title="AI Chat History",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    /* Streamlit 기본 사이드바 네비게이션(상단 파일명 목록 및 구분선) 숨기기 */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================
# 1. SQLite 데이터베이스 조회 및 관리 헬퍼 함수
# =============================================================
DB_PATH = "chat_history.db"

def get_all_sessions():
    """모든 세션 목록(최대 10개)을 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id, title, turn_count, updated_at FROM chat_sessions ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_messages_df(session_id=None):
    """세션별 또는 전체 대화 기록을 데이터프레임으로 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    if session_id and session_id != "ALL":
        query = """
            SELECT id, session_id, role, content, has_image, created_at 
            FROM chat_messages 
            WHERE session_id = ?
            ORDER BY id ASC
        """
        df = pd.read_sql_query(query, conn, params=(session_id,))
    else:
        query = """
            SELECT id, session_id, role, content, has_image, created_at 
            FROM chat_messages 
            ORDER BY id ASC
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def delete_single_session(session_id):
    """지정한 특정 세션과 관련 메시지를 영구 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
    cursor.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))
    conn.commit()
    conn.close()

def cleanup_old_sessions():
    """최대 10개의 세션만 유지하며, 10개를 초과하면 가장 오래된 세션부터 자동 영구 삭제(FIFO)합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT session_id FROM chat_sessions ORDER BY updated_at DESC")
    sessions = cursor.fetchall()
    
    if len(sessions) > 10:
        old_sessions = sessions[10:]
        old_ids = [s[0] for s in old_sessions]
        placeholders = ",".join("?" * len(old_ids))
        cursor.execute(f"DELETE FROM chat_messages WHERE session_id IN ({placeholders})", old_ids)
        cursor.execute(f"DELETE FROM chat_sessions WHERE session_id IN ({placeholders})", old_ids)
        conn.commit()
    conn.close()

def clear_all_history():
    """SQLite DB의 모든 세션 및 대화 기록을 완전히 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages")
    cursor.execute("DELETE FROM chat_sessions")
    conn.commit()
    conn.close()

def insert_sample_session():
    """테스트용 샘플 세션(3회 턴 = 6건 대화)을 DB에 추가합니다."""
    new_sid = f"sess_sample_{datetime.now().strftime('%H%M%S')}_{uuid.uuid4().hex[:6]}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1) 세션 생성
    cursor.execute(
        "INSERT INTO chat_sessions (session_id, title, turn_count) VALUES (?, ?, ?)",
        (new_sid, "샘플 Streamlit 질의응답", 3)
    )
    
    # 2) 대화 6건 삽입
    samples = [
        (new_sid, "user", "안녕하세요! 파이썬 Streamlit으로 웹 앱을 만드는 중입니다.", 0),
        (new_sid, "assistant", "안녕하세요! Streamlit은 파이썬만으로 빠르게 인터랙티브 웹 앱을 구축할 수 있는 훌륭한 프레임워크입니다. 어떤 기능을 만들고 계신가요?", 0),
        (new_sid, "user", "이 사진에 있는 로고를 분석해줘.", 1),
        (new_sid, "assistant", "첨부해주신 이미지를 분석했습니다. Streamlit의 시그니처 레드 컬러와 심볼 마크가 포함되어 있네요!", 1),
        (new_sid, "user", "SQLite와 연동해서 대화 기록을 10개 세션만 보관하는 방법도 알려줘.", 0),
        (new_sid, "assistant", "FIFO 쿼리를 적용하여 세션 수가 10개를 초과할 때 가장 오래된 세션과 대화를 자동 삭제하면 깔끔하게 유지할 수 있습니다.", 0),
    ]
    cursor.executemany("INSERT INTO chat_messages (session_id, role, content, has_image) VALUES (?, ?, ?, ?)", samples)
    conn.commit()
    conn.close()
    cleanup_old_sessions()

# =============================================================
# 2. 메인 헤더 및 보안 취약성 안내문
# =============================================================
st.markdown("## 📜 AI Studio 대화 내역 보관함")
st.caption("SQLite 데이터베이스(chat_history.db)에 영구 저장된 최근 10개 세션의 대화 기록을 탐색하고 관리합니다.")

# 보안 취약점 안내 메시지 (채팅 내역 살펴보기)
st.info("""
🛡️ **로컬 데이터베이스 보안 및 보관 정책 안내**
- **공유 환경 주의**: 대화 기록은 서버 로컬 SQLite 데이터베이스에 보관됩니다. 공용 컴퓨터나 다중 사용자 환경에서는 타인이 대화 내역을 열람할 수 있으니 민감한 대화는 삭제해 주세요.
- **자동 보관 정책**: 최근 **10개의 대화 세션**만 보관되며, 새 세션이 추가되면 가장 오래된 세션부터 자동 삭제(FIFO)됩니다.
- **세션 용량 정책**: 각 세션당 최대 **100회(턴)** 대화만 보관됩니다.
""", icon="ℹ️")

# DB에서 전체 세션 목록 가져오기
sessions_list = get_all_sessions()
session_count = len(sessions_list)

# =============================================================
# 3. 사이드바: 네비게이션, 검색/필터 및 데이터 관리
# =============================================================
with st.sidebar:
    # 1. 일관된 브랜드 헤더 및 네비게이션 메뉴 (최상단)
    st.markdown("### ✨ AI Studio")
    st.caption("멀티모달 챗봇 & 대화 관리 시스템")
    
    st.markdown("#### 🧭 메뉴")
    st.page_link("app2.py", label="AI 채팅 (Chat)", icon="💬")
    st.page_link("pages/app2_history.py", label="대화 내역 보관함 (History)", icon="📜")
    
    st.divider()
    
    # 2. 대화 내역 필터
    st.markdown("#### 🔍 대화 내역 필터")
    
    # 세션 선택기
    session_select_options = ["ALL"] + [s[0] for s in sessions_list]
    session_labels = {"ALL": "🌐 전체 세션 통합 보기"}
    for s in sessions_list:
        session_labels[s[0]] = f"📁 {s[1]} ({s[2]}/100회)"
        
    selected_filter_session = st.selectbox(
        label="조회할 세션 선택",
        options=session_select_options,
        index=0,
        format_func=lambda sid: session_labels.get(sid, sid)
    )
    
    # 키워드 검색
    search_query = st.text_input("대화 내용 키워드 검색", placeholder="검색어를 입력하세요...")
    
    # 역할별 필터링
    role_filter = st.selectbox("작성자 선택", options=["전체", "사용자 (User)", "AI (Assistant)"])
    
    # 이미지 포함 대화만 보기 체크박스
    only_images = st.checkbox("이미지 첨부된 대화만 보기", value=False)
    
    # 정렬 기준
    sort_order = st.radio("정렬 순서", options=["시간순 (과거 → 최신)", "역순 (최신 → 과거)"])
    
    st.divider()
    
    # 3. 데이터 관리 기능
    st.markdown("#### 🛠️ 데이터 관리")
    
    if selected_filter_session != "ALL":
        if st.button("🗑️ 현재 선택한 세션 삭제", use_container_width=True, help="현재 선택된 세션과 해당 대화를 DB에서 삭제합니다."):
            delete_single_session(selected_filter_session)
            st.warning("선택한 세션이 삭제되었습니다.")
            st.rerun()

    if st.button("🧪 샘플 세션 데이터 추가", use_container_width=True, help="테스트용 샘플 세션(3회 턴 = 6건)을 DB에 삽입합니다."):
        insert_sample_session()
        st.success("샘플 세션이 추가되었습니다!")
        st.rerun()
        
    if st.button("💥 전체 대화 내역 영구 삭제", use_container_width=True, help="DB의 모든 세션과 대화 기록을 지웁니다."):
        clear_all_history()
        st.warning("모든 대화 기록이 영구 삭제되었습니다.")
        st.rerun()

# =============================================================
# 4. 데이터 로드 및 상단 핵심 메트릭 지표
# =============================================================
df = get_messages_df(selected_filter_session)
total_count = len(df)

# 상단 통계 지표 (st.metric)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
user_count = len(df[df["role"] == "user"]) if total_count > 0 else 0
ai_count = len(df[df["role"] == "assistant"]) if total_count > 0 else 0
image_count = len(df[df["has_image"] == 1]) if total_count > 0 else 0

with col_m1:
    st.metric(label="보관된 세션 수", value=f"{session_count} / 10개")
with col_m2:
    if selected_filter_session != "ALL":
        curr_turns = user_count
        st.metric(label="현재 세션 턴 수", value=f"{curr_turns} / 100회")
    else:
        st.metric(label="총 메시지 수", value=f"{total_count}개")
with col_m3:
    st.metric(label="사용자 질문", value=f"{user_count}건")
with col_m4:
    st.metric(label="이미지 첨부 대화", value=f"{image_count}건")

st.divider()

# =============================================================
# 5. 데이터 필터링 로직
# =============================================================
filtered_df = df.copy()

if total_count > 0:
    # 1) 검색어 필터
    if search_query:
        filtered_df = filtered_df[filtered_df["content"].str.contains(search_query, case=False, na=False)]
    
    # 2) 역할 필터
    if role_filter == "사용자 (User)":
        filtered_df = filtered_df[filtered_df["role"] == "user"]
    elif role_filter == "AI (Assistant)":
        filtered_df = filtered_df[filtered_df["role"] == "assistant"]
        
    # 3) 이미지 필터
    if only_images:
        filtered_df = filtered_df[filtered_df["has_image"] == 1]
        
    # 4) 정렬
    if sort_order == "역순 (최신 → 과거)":
        filtered_df = filtered_df.sort_values(by="id", ascending=False)
    else:
        filtered_df = filtered_df.sort_values(by="id", ascending=True)

# =============================================================
# 6. 본문: 탭 분리 화면 (대화형 뷰 vs 테이블 뷰)
# =============================================================
if len(filtered_df) == 0:
    st.info("💡 표시할 대화 내역이 없습니다. 사이드바의 '🧪 샘플 세션 데이터 추가' 버튼을 눌러보거나 AI 채팅 화면에서 대화를 시작해보세요!")
else:
    tab_chat, tab_table = st.tabs(["💬 메신저 형태 뷰 (Chat View)", "📊 데이터 표 및 내보내기 (Table View)"])

    # (1) 메신저 형태 대화 뷰
    with tab_chat:
        st.caption(f"총 **{len(filtered_df)}건**의 메시지가 검색되었습니다.")
        
        for _, row in filtered_df.iterrows():
            role = row["role"]
            avatar = "👤" if role == "user" else "✨"
            role_name = "사용자" if role == "user" else "AI 어시스턴트"
            
            with st.chat_message(role, avatar=avatar):
                col_h_left, col_h_right = st.columns([4, 1.5])
                with col_h_left:
                    st.markdown(f"**{role_name}** `#{row['id']}` · `세션: {row['session_id'][:16]}`")
                with col_h_right:
                    st.caption(f"🕒 {row['created_at']}")
                    
                if row["has_image"]:
                    st.info("📷 이미지가 첨부된 메시지입니다.", icon="🖼️")
                    
                st.markdown(row["content"])

    # (2) 데이터 테이블 뷰 및 CSV 다운로드
    with tab_table:
        st.subheader("데이터베이스 원본 표")
        st.dataframe(filtered_df, width="stretch", hide_index=True)
        
        csv_data = filtered_df.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 대화 내역 CSV 파일로 다운로드 (UTF-8)",
            data=csv_data,
            file_name=f"chat_history_{selected_filter_session}.csv",
            mime="text/csv"
        )
