import streamlit as st
from .typography import show_typography
from .rich_text import show_rich_text

def show_text_tabs():
    """텍스트 및 서식(Text elements) 하위 탭들을 생성하고 각 화면을 연결합니다."""
    sub_tab1, sub_tab2 = st.tabs([
        "🔤 타이포그래피 & 구분선",
        "💻 마크다운 · 코드 · 수식"
    ])

    with sub_tab1:
        show_typography()

    with sub_tab2:
        show_rich_text()

