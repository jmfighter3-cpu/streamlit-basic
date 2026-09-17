import streamlit as st
import sqlite3
import pandas as pd

# =============================================================
# 0. 페이지 설정 및 모던 스타일링
# =============================================================
st.set_page_config(
    page_title="과거 대화 보관함",
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
# 1. SQLite 데이터베이스 조회 헬퍼 함수
# =============================================================
DB_PATH = "chat_history.db"

def get_all_messages():
    """SQLite DB에서 모든 대화 기록을 데이터프레임으로 가져옵니다."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT id, role, content, has_image, created_at 
        FROM chat_messages 
        ORDER BY id ASC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def clear_all_history():
    """SQLite DB의 모든 대화 기록을 삭제합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_messages")
    conn.commit()
    conn.close()

def insert_sample_data():
    """테스트를 위한 샘플 대화 데이터를 DB에 추가합니다."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    samples = [
        ("user", "안녕하세요! 파이썬 Streamlit으로 웹 앱을 만드는 중입니다.", 0),
        ("assistant", "안녕하세요! Streamlit은 파이썬만으로 빠르게 인터랙티브 웹 앱을 구축할 수 있는 훌륭한 프레임워크입니다. 어떤 기능을 만들고 계신가요?", 0),
        ("user", "이 사진에 있는 로고를 분석해줘.", 1),
        ("assistant", "첨부해주신 이미지를 분석했습니다. Streamlit의 시그니처 레드 컬러와 심볼 마크가 포함되어 있네요!", 1),
        ("user", "SQLite와 연동해서 대화 기록을 저장하는 방법도 알려줘.", 0),
        ("assistant", "파이썬 내장 sqlite3 라이브러리를 사용하면 별도 서버 없이 파일 하나(chat_history.db)로 손쉽게 저장할 수 있습니다.", 0),
    ]
    cursor.executemany("INSERT INTO chat_messages (role, content, has_image) VALUES (?, ?, ?)", samples)
    conn.commit()
    conn.close()

# =============================================================
# 2. 메인 헤더
# =============================================================
st.markdown("## 📜 AI Studio 대화 내역 보관함")
st.caption("SQLite 데이터베이스(chat_history.db)에 영구 저장된 대화 기록을 탐색하고 관리합니다.")

# DB에서 전체 대화 불러오기
df = get_all_messages()
total_count = len(df)

# 상단 핵심 통계 지표 (st.metric)
col_m1, col_m2, col_m3, col_m4 = st.columns(4)
user_count = len(df[df["role"] == "user"]) if total_count > 0 else 0
ai_count = len(df[df["role"] == "assistant"]) if total_count > 0 else 0
image_count = len(df[df["has_image"] == 1]) if total_count > 0 else 0

with col_m1:
    st.metric(label="총 메시지 수", value=f"{total_count}개")
with col_m2:
    st.metric(label="사용자 질문", value=f"{user_count}건")
with col_m3:
    st.metric(label="AI 답변", value=f"{ai_count}건")
with col_m4:
    st.metric(label="이미지 첨부 대화", value=f"{image_count}건")

st.divider()

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
    if st.button("🧪 샘플 대화 데이터 추가", use_container_width=True, help="테스트용 대화 데이터 6건을 DB에 삽입합니다."):
        insert_sample_data()
        st.success("샘플 데이터가 추가되었습니다!")
        st.rerun()
        
    if st.button("🗑️ 전체 대화 내역 영구 삭제", use_container_width=True, help="DB의 모든 대화 기록을 지웁니다."):
        clear_all_history()
        st.warning("모든 대화 기록이 삭제되었습니다.")
        st.rerun()

# =============================================================
# 4. 데이터 필터링 로직
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
# 5. 본문: 탭 분리 화면 (대화형 뷰 vs 테이블 뷰)
# =============================================================
if len(filtered_df) == 0:
    st.info("💡 표시할 대화 내역이 없습니다. 사이드바의 '🧪 샘플 대화 데이터 추가' 버튼을 눌러보거나 app2.py에서 새 대화를 시작해보세요!")
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
                col_h_left, col_h_right = st.columns([4, 1])
                with col_h_left:
                    st.markdown(f"**{role_name}** `#{row['id']}`")
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
            label="📥 대화 내역 CSV 파일로 다운로드",
            data=csv_data,
            file_name="chat_history_export.csv",
            mime="text/csv"
        )

