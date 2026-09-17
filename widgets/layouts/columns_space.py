import streamlit as st

def show_columns_space():
    """컬럼 배치(st.columns)와 여백(st.space) 위젯을 화면에 표시합니다."""
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
        st.write("👉 **넓은 컬럼 (비율 2)**: 본문이나 주요 콘텐츠를 배치합니다.")
    with col_narrow:
        st.write("👉 **좁은 컬럼 (비율 1)**: 부가 정보를 배치합니다.")

    st.divider()

    st.subheader("2. 여백 조절 (st.space)")
    st.caption("위젯과 위젯 사이에 자연스러운 빈 공간(여백)을 추가합니다.")

    st.write("첫 번째 텍스트 블록")
    st.space("medium")  # 중간 크기 세로 여백 추가
    st.write("두 번째 텍스트 블록 (위 텍스트와 사이에 st.space('medium') 여백이 적용됨)")

