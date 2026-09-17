import streamlit as st
from .line_area_charts import show_line_area_charts
from .bar_scatter_charts import show_bar_scatter_charts
from .map_charts import show_map_charts

def show_chart_tabs():
    """차트 및 시각화(Chart elements) 하위 탭들을 생성하고 각 화면을 연결합니다."""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📈 선 & 영역 차트",
        "📊 막대 & 산점도 차트",
        "🗺️ 지도 시각화"
    ])

    with sub_tab1:
        show_line_area_charts()

    with sub_tab2:
        show_bar_scatter_charts()

    with sub_tab3:
        show_map_charts()

