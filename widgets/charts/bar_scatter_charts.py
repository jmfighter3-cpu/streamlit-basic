import streamlit as st
import pandas as pd

def show_bar_scatter_charts():
    """st.bar_chart와 st.scatter_chart 예시입니다."""
    st.subheader("1. 막대 그래프 (st.bar_chart)")
    st.caption("카테고리별 수치 크기를 직관적으로 비교할 때 사용합니다.")

    fruit_sales = pd.DataFrame({
        "과일": ["사과", "바나나", "오렌지", "포도", "딸기"],
        "판매량": [120, 95, 80, 150, 200]
    })
    st.bar_chart(fruit_sales, x="과일", y="판매량")

    st.divider()

    st.subheader("2. 산점도 그래프 (st.scatter_chart)")
    st.caption("두 변수 간의 분포와 상관관계를 점(Point)으로 표현합니다.")

    study_data = pd.DataFrame({
        "공부시간": [2, 3, 4, 5, 6, 7, 8, 9, 10],
        "시험점수": [55, 60, 68, 75, 78, 85, 90, 95, 98]
    })
    st.scatter_chart(study_data, x="공부시간", y="시험점수")

