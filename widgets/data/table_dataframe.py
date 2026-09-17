import streamlit as st
import pandas as pd

def show_table_dataframe():
    """st.dataframe과 st.table을 활용한 데이터 표 표시 예시입니다."""
    st.subheader("1. 인터랙티브 데이터프레임 (st.dataframe)")
    st.caption("컬럼 정렬, 검색, 크기 조절이 가능한 대화형 표입니다.")

    # 예시용 간단한 데이터프레임 생성
    sample_df = pd.DataFrame({
        "이름": ["홍길동", "이순신", "강감찬", "유관순"],
        "나이": [25, 45, 52, 19],
        "직업": ["개발자", "장군", "관료", "학생"],
        "점수": [88, 95, 90, 92]
    })

    # st.dataframe()으로 표 출력 (width='stretch'로 가로 너비에 맞춤)
    st.dataframe(sample_df, width="stretch")

    st.divider()

    st.subheader("2. 정적 표 (st.table)")
    st.caption("정렬이나 조작 없이 화면에 그대로 깔끔하게 고정되어 출력되는 표입니다.")

    # st.table()로 정적 표 출력
    st.table(sample_df)
