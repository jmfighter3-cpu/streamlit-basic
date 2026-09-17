import streamlit as st

def show_selection_widgets():
    """선택 및 버튼 관련 위젯들을 화면에 표시합니다."""
    st.subheader("1. 버튼 (st.button)")
    # st.button()은 클릭하는 순간 True가 되고 이후 다시 False로 돌아갑니다.
    # - type: "secondary"(기본 회색) 또는 "primary"(강조 색상)
    if st.button("일반 버튼 클릭"):
        st.write("🎉 일반 버튼을 클릭했습니다!")

    if st.button("강조 버튼 클릭", type="primary"):
        st.write("🔥 강조(Primary) 버튼을 클릭했습니다!")

    st.divider()

    st.subheader("2. 체크박스 & 토글 (st.checkbox, st.toggle)")
    # st.checkbox()는 참/거짓(True/False)을 선택하는 기본 체크박스입니다.
    agree = st.checkbox("이용약관에 동의합니다", value=False)
    st.write(f"👉 약관 동의 상태: **{agree}**")

    # st.toggle()은 세련된 온/오프 스위치 위젯입니다.
    is_active = st.toggle("알림 받기", value=True)
    st.write(f"👉 알림 설정 상태: **{'켜짐(ON)' if is_active else '꺼짐(OFF)'}**")

    st.divider()

    st.subheader("3. 라디오 버튼 (st.radio)")
    # st.radio()는 여러 옵션 중 하나만 선택할 때 사용합니다.
    # - options: 선택 항목 목록
    # - index: 기본 선택 항목 인덱스 (0부터 시작)
    food = st.radio(
        label="가장 좋아하는 음식",
        options=["피자", "치킨", "초밥", "떡볶이"],
        index=0
    )
    st.write(f"👉 선택한 음식: **{food}**")

    st.divider()

    st.subheader("4. 드롭다운 선택 (st.selectbox, st.multiselect)")
    # st.selectbox()는 드롭다운 메뉴에서 1개를 선택합니다.
    city = st.selectbox(
        label="거주 지역 선택",
        options=["서울", "부산", "대구", "인천", "광주", "대전"]
    )
    st.write(f"👉 선택한 지역: **{city}**")

    # st.multiselect()는 여러 개를 동시에 선택할 수 있는 드롭다운입니다.
    # - default: 기본으로 선택되어 있을 항목 리스트
    skills = st.multiselect(
        label="관심 있는 프로그래밍 분야 (다중 선택)",
        options=["파이썬", "데이터 분석", "머신러닝", "웹 개발", "모바일 앱"],
        default=["파이썬"]
    )
    st.write(f"👉 선택한 관심 분야: **{skills}**")

