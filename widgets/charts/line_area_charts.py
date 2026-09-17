import streamlit as st
import pandas as pd
import numpy as np

def show_line_area_charts():
    """st.line_chart와 st.area_chart 예시입니다."""
    st.subheader("1. 꺾은선 그래프 (st.line_chart)")
    st.caption("시간의 흐름이나 추세를 선으로 명확하게 보여줍니다.")

    # 10일간의 기온 데이터 예시
    chart_data = pd.DataFrame({
        "서울": [15, 17, 19, 18, 22, 24, 21, 23, 25, 26],
        "부산": [18, 19, 21, 20, 23, 25, 23, 24, 26, 27]
    })
    st.line_chart(chart_data)

    st.divider()

    st.subheader("2. 영역 그래프 (st.area_chart)")
    st.caption("선 아래의 영역을 채워 누적 수치나 볼륨감을 시각적으로 강조합니다.")

    st.area_chart(chart_data)

