import streamlit as st

# @st.dialog 데코레이터를 붙인 함수는 화면 중앙에 독립적인 모달 팝업으로 뜹니다.
@st.dialog("회원 가입 팝업")
def signup_dialog():
    st.write("화면 중앙에 독립적으로 뜨는 모달 팝업 창입니다.")
    user_name = st.text_input("이름")
    user_email = st.text_input("이메일")
    if st.button("가입 완료"):
        st.success(f"{user_name}님 환영합니다! ({user_email})")


def show_popups_dialog():
    """모달 다이얼로그(st.dialog)와 팝오버(st.popover)를 화면에 표시합니다."""
    st.subheader("1. 모달 팝업 다이얼로그 (st.dialog)")
    st.caption("버튼을 누르면 화면 중앙에 팝업 대화상자가 열립니다.")

    if st.button("팝업 창 열기"):
        signup_dialog()

    st.divider()

    st.subheader("2. 팝오버 메뉴 (st.popover)")
    st.caption("버튼을 클릭하면 말풍선처럼 작은 오버레이 창이 열립니다.")

    with st.popover("⚙️ 화면 환경설정 열기"):
        st.write("빠른 설정 메뉴")
        show_tips = st.checkbox("도움말 툴팁 항상 보기", value=True)
        st.write(f"현재 설정 상태: {show_tips}")

