import streamlit as st
from .alert_boxes import show_alert_boxes
from .progress_spinner import show_progress_spinner
from .celebration_toast import show_celebration_toast

def show_status_tabs():
    """상태 및 알림(Status elements) 하위 탭들을 생성하고 각 화면을 연결합니다."""
    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "💬 알림 상자 (Alerts)",
        "⏳ 진행률 & 로딩 (Progress)",
        "🎉 축하 & 토스트 (Effects)"
    ])

    with sub_tab1:
        show_alert_boxes()

    with sub_tab2:
        show_progress_spinner()

    with sub_tab3:
        show_celebration_toast()

