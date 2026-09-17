import streamlit as st

def show_containers_expander():
    """컨테이너(st.container)와 익스팬더(st.expander)를 화면에 표시합니다."""
    st.subheader("1. 컨테이너 (st.container)")
    st.caption("여러 요소를 하나의 블록으로 묶거나, 테두리(border) 및 스크롤(height) 상자를 만듭니다.")

    # (1) border=True: 테두리가 있는 카드형 컨테이너
    with st.container(border=True):
        st.write("📦 **테두리가 있는 카드형 컨테이너 (border=True)**")
        st.write("관련된 위젯들을 깔끔하게 묶어 카드로 보여줄 때 유용합니다.")

    # (2) height=100: 고정 높이 스크롤 상자
    with st.container(height=100, border=True):
        st.write("📜 **스크롤 가능한 고정 높이 컨테이너 (height=100)**")
        st.write("상자 안의 내용이 길어지면 자동으로 스크롤바가 생성됩니다.")
        st.write("내용 1...")
        st.write("내용 2...")
        st.write("내용 3...")

    st.divider()

    st.subheader("2. 접기 / 펼치기 (st.expander)")
    st.caption("상세 설명이나 긴 부가 정보를 클릭 시에만 펼쳐보도록 숨겨둡니다.")

    with st.expander(label="📌 자주 묻는 질문(FAQ) 클릭해서 열기", expanded=False):
        st.write("Q: Streamlit 레이아웃의 가장 큰 장점은 무엇인가요?")
        st.write("A: HTML/CSS를 몰라도 파이썬의 with 구문 하나로 깔끔한 배치가 완성된다는 점입니다!")

