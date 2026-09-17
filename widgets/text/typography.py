import streamlit as st

def show_typography():
    """st.title, st.header, st.subheader, st.caption, st.text, st.divider 예시입니다."""
    st.subheader("타이포그래피 및 서식 요소")
    st.caption("텍스트의 위계와 가독성을 높여주는 기본 서식 요소들입니다.")

    st.title("메인 제목 (st.title)")
    st.header("대제목 (st.header)")
    st.subheader("중제목 (st.subheader)")
    st.caption("작은 설명이나 출처를 적는 캡션 (st.caption)")
    st.text("고정폭 글꼴로 있는 그대로 출력되는 기본 텍스트 (st.text)")

    st.divider()  # 수평선 구분선
    st.write("위의 가로선은 `st.divider()`로 생성되었습니다.")

