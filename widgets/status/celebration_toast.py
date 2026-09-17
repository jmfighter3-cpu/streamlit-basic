import streamlit as st

def show_celebration_toast():
    """st.toast, st.balloons, st.snow 예시입니다."""
    st.subheader("1. 토스트 알림 (st.toast)")
    st.caption("화면 우측 하단에 일시적으로 떠오르는 팝업 메시지입니다.")

    if st.button("토스트 알림 띄우기"):
        st.toast("메시지가 성공적으로 전송되었습니다!", icon="📨")

    st.divider()

    st.subheader("2. 풍선 축하 효과 (st.balloons)")
    st.caption("화면 아래에서 위로 다채로운 풍선들이 떠오르는 애니메이션 효과입니다.")

    if st.button("🎈 풍선 날리기"):
        st.balloons()

    st.divider()

    st.subheader("3. 눈송이 효과 (st.snow)")
    st.caption("화면 위에서 아래로 눈송이가 흩날리는 겨울 테마 애니메이션 효과입니다.")

    if st.button("❄️ 눈 내리기"):
        st.snow()

