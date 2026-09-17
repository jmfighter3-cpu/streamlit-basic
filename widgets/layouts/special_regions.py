import streamlit as st

def show_special_regions():
    """사이드바(st.sidebar), 하단 고정(st.bottom), 동적 교체(st.empty)를 화면에 표시합니다."""
    st.subheader("1. 동적 내용 교체 (st.empty)")
    st.caption("한 번 출력한 위치의 내용을 지우거나 새로운 내용으로 덮어씁니다.")

    placeholder = st.empty()
    placeholder.info("초기 상태 메시지입니다.")

    if st.button("메시지 내용 교체하기"):
        placeholder.success("🎉 버튼 클릭으로 기존 메시지가 새 메시지로 교체되었습니다!")

    st.divider()

    st.subheader("2. 좌측 사이드바 (st.sidebar)")
    st.caption("화면 좌측 사이드바 패널에 위젯을 배치합니다. (좌측 화면 확인)")

    st.sidebar.title("📁 사이드바 영역")
    st.sidebar.write("`st.sidebar`를 통해 좌측 메뉴바에 독립적으로 위젯을 올릴 수 있습니다.")
    st.sidebar.text_input("사이드바 검색어", placeholder="검색어를 입력하세요")

    st.divider()

    st.subheader("3. 하단 고정 영역 (st.bottom)")
    st.caption("브라우저 창 맨 밑바닥에 고정되어 떠 있는 영역입니다. (화면 최하단 확인)")
    st.bottom.info("🔔 이 알림은 `st.bottom`으로 브라우저 창 최하단에 고정되어 표시됩니다.")

