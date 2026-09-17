import streamlit as st

# -------------------------------------------------------------
# 3. st.dialog: 모달 팝업 다이얼로그
# -------------------------------------------------------------
# @st.dialog 데코레이터를 함수 위에 붙이면 해당 함수가 화면 중앙에 모달 팝업으로 열립니다.
@st.dialog("회원 가입 팝업")
def signup_dialog():
    st.write("화면 중앙에 독립적으로 뜨는 모달 팝업 창입니다.")
    user_name = st.text_input("이름")
    user_email = st.text_input("이메일")
    if st.button("가입 완료"):
        st.success(f"{user_name}님 환영합니다! ({user_email})")


def show_layout_widgets():
    """공식 문서(Layouts and containers)의 모든 레이아웃 요소를 시연합니다."""
    
    # -------------------------------------------------------------
    # 1. st.columns: 다중 열(컬럼) 나란히 배치
    # -------------------------------------------------------------
    st.subheader("1. 컬럼 나란히 배치 (st.columns)")
    st.caption("화면을 가로로 분할하여 여러 요소를 옆으로 나란히 배치합니다.")

    # 동일한 크기로 3분할 배치
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("왼쪽 컬럼 (1/3)")
        st.button("왼쪽 버튼")
    with col2:
        st.success("가운데 컬럼 (2/3)")
        st.text_input("가운데 입력", key="col_mid")
    with col3:
        st.warning("오른쪽 컬럼 (3/3)")
        st.checkbox("오른쪽 체크", key="col_right")

    # 비율 지정 분할 배치 (2:1 비율)
    col_wide, col_narrow = st.columns([2, 1])
    with col_wide:
        st.write("👉 **넓은 컬럼 (비율 2)**: 긴 내용이나 주요 콘텐츠를 배치하기 좋습니다.")
    with col_narrow:
        st.write("👉 **좁은 컬럼 (비율 1)**: 보조 요소를 배치합니다.")

    st.divider()

    # -------------------------------------------------------------
    # 2. st.container: 컨테이너 상자 (테두리 및 스크롤)
    # -------------------------------------------------------------
    st.subheader("2. 컨테이너 (st.container)")
    st.caption("여러 요소를 하나의 블록으로 묶거나, 테두리(border) 및 스크롤(height) 상자를 만듭니다.")

    # (1) border=True: 테두리가 있는 카드형 컨테이너
    with st.container(border=True):
        st.write("📦 **테두리가 있는 카드형 컨테이너**")
        st.write("서로 관련된 입력 위젯이나 설명을 하나로 묶어줄 때 아주 유용합니다.")

    # (2) height=100: 고정 높이 스크롤 컨테이너
    with st.container(height=100, border=True):
        st.write("📜 **스크롤이 가능한 고정 높이 컨테이너**")
        st.write("내용이 많아지면 상자 안에서 스크롤바가 생깁니다.")
        st.write("줄바꿈 1...")
        st.write("줄바꿈 2...")
        st.write("줄바꿈 3...")

    st.divider()

    # -------------------------------------------------------------
    # 3. st.dialog 실행 버튼
    # -------------------------------------------------------------
    st.subheader("3. 모달 팝업 다이얼로그 (st.dialog)")
    st.caption("버튼을 누르면 화면 중앙에 팝업 창이 뜹니다.")
    if st.button("팝업 창 열기"):
        signup_dialog()

    st.divider()

    # -------------------------------------------------------------
    # 4. st.expander: 접기 / 펼치기 아코디언
    # -------------------------------------------------------------
    st.subheader("4. 접기 / 펼치기 (st.expander)")
    st.caption("상세 설명이나 부가적인 내용을 필요할 때만 펼쳐보도록 숨겨둡니다.")

    with st.expander(label="📌 자주 묻는 질문(FAQ) 클릭해서 열기", expanded=False):
        st.write("Q: Streamlit은 배우기 쉬운가요?")
        st.write("A: 네! 파이썬 기본 문법만 알면 누구나 멋진 웹 앱을 빠르게 만들 수 있습니다.")

    st.divider()

    # -------------------------------------------------------------
    # 5. st.popover: 팝오버 팝업 메뉴
    # -------------------------------------------------------------
    st.subheader("5. 팝오버 메뉴 (st.popover)")
    st.caption("버튼을 클릭하면 말풍선처럼 작은 오버레이 상자가 열립니다.")

    with st.popover("⚙️ 화면 환경설정 열기"):
        st.write("빠른 설정 메뉴")
        show_tips = st.checkbox("도움말 툴팁 항상 보기", value=True)
        st.write(f"설정 상태: {show_tips}")

    st.divider()

    # -------------------------------------------------------------
    # 6. st.empty: 동적 자리표시자 (내용 교체)
    # -------------------------------------------------------------
    st.subheader("6. 동적 내용 교체 (st.empty)")
    st.caption("한 번 출력한 위치의 내용을 다른 내용으로 덮어쓰거나 비울 때 사용합니다.")

    placeholder = st.empty()
    placeholder.info("초기 상태 메시지입니다.")

    if st.button("메시지 내용 교체하기"):
        placeholder.success("🎉 버튼 클릭으로 기존 메시지가 새 메시지로 교체되었습니다!")

    st.divider()

    # -------------------------------------------------------------
    # 7. st.space: 여백 추가
    # -------------------------------------------------------------
    st.subheader("7. 여백 조절 (st.space)")
    st.caption("위젯과 위젯 사이에 자연스러운 빈 공간(여백)을 추가합니다.")

    st.write("첫 번째 텍스트")
    st.space("medium")  # 중간 크기 여백 추가
    st.write("두 번째 텍스트 (위 텍스트 사이에 st.space('medium') 여백이 적용됨)")

    st.divider()

    # -------------------------------------------------------------
    # 8. st.sidebar: 좌측 사이드바
    # -------------------------------------------------------------
    st.subheader("8. 사이드바 (st.sidebar)")
    st.caption("화면 좌측 사이드바 패널에 위젯들을 배치합니다. (좌측 화면 확인)")

    st.sidebar.title("📁 사이드바 영역")
    st.sidebar.write("`st.sidebar`를 사용하면 좌측 메뉴바에 위젯을 올릴 수 있습니다.")
    st.sidebar.text_input("사이드바 검색어", placeholder="검색어를 입력하세요")

    # -------------------------------------------------------------
    # 9. st.bottom: 화면 하단 고정 영역
    # -------------------------------------------------------------
    st.subheader("9. 하단 고정 영역 (st.bottom)")
    st.caption("브라우저 창 맨 밑바닥에 고정되어 떠 있는 영역입니다. (화면 최하단 확인)")
    st.bottom.info("🔔 이 알림은 `st.bottom`으로 브라우저 창 최하단에 고정되어 표시됩니다.")

