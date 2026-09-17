import streamlit as st
from .text_widgets import show_text_widgets
from .selection_widgets import show_selection_widgets
from .number_slider_widgets import show_number_slider_widgets
from .datetime_widgets import show_datetime_widgets

def show_input_tabs():
    """인풋 위젯 하위 탭들을 생성하고 각 위젯 화면을 표시합니다."""
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📝 텍스트 입력",
        "🔘 선택 & 버튼",
        "🔢 숫자 & 슬라이더",
        "📅 날짜 · 시간 · 색상"
    ])

    with sub_tab1:
        show_text_widgets()

    with sub_tab2:
        show_selection_widgets()

    with sub_tab3:
        show_number_slider_widgets()

    with sub_tab4:
        show_datetime_widgets()

