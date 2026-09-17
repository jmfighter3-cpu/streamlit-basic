import streamlit as st
from .columns_space import show_columns_space
from .containers_expander import show_containers_expander
from .popups_dialog import show_popups_dialog
from .special_regions import show_special_regions

def show_layout_tabs():
    """레이아웃 & 컨테이너 하위 탭들을 생성하고 각 레이아웃 화면을 표시합니다."""
    sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
        "📊 컬럼 & 여백 (Columns & Space)",
        "📦 컨테이너 & 접기 (Container & Expander)",
        "💬 팝업 & 모달 (Dialog & Popover)",
        "📌 특수 영역 (Sidebar · Bottom · Empty)"
    ])

    with sub_tab1:
        show_columns_space()

    with sub_tab2:
        show_containers_expander()

    with sub_tab3:
        show_popups_dialog()

    with sub_tab4:
        show_special_regions()

