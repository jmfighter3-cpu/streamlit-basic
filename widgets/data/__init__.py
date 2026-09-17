import streamlit as st
from .table_dataframe import show_table_dataframe
from .metric_widgets import show_metric_widgets
from .json_dict import show_json_dict

def show_data_tabs():
    """데이터 표시(Data elements) 하위 탭들을 생성하고 각 화면을 연결합니다."""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "📋 표 & 데이터프레임",
        "📌 지표 (Metric)",
        "🌳 JSON 계층 구조"
    ])

    with sub_tab1:
        show_table_dataframe()

    with sub_tab2:
        show_metric_widgets()

    with sub_tab3:
        show_json_dict()

