import streamlit as st

# 분리된 각 대분류 탭 총괄 모듈들 불러오기
from widgets.inputs import show_input_tabs
from widgets.layouts import show_layout_tabs
from widgets.data import show_data_tabs
from widgets.charts import show_chart_tabs
from widgets.status import show_status_tabs
from widgets.text import show_text_tabs
from widgets.media import show_media_tabs

# =============================================================
# Streamlit 공식 API 핵심 요소 종합 쇼케이스
# =============================================================
st.title("🎈 Streamlit 종합 쇼케이스")
st.caption("공식 API 레퍼런스의 핵심 카테고리를 계층형 탭 구조로 한눈에 둘러보고 체험할 수 있습니다.")

# 최상위 7대 대분류 탭 생성
(
    tab_inputs,
    tab_layouts,
    tab_data,
    tab_charts,
    tab_status,
    tab_text,
    tab_media
) = st.tabs([
    "🎮 인풋 위젯",
    "📐 레이아웃",
    "📊 데이터 표시",
    "📈 차트 시각화",
    "🔔 상태 & 알림",
    "📄 텍스트 & 서식",
    "🖼️ 미디어"
])

# 1. 인풋 위젯 대분류 (텍스트, 선택, 숫자, 날짜/시간)
with tab_inputs:
    show_input_tabs()

# 2. 레이아웃 & 컨테이너 대분류 (컬럼, 컨테이너, 다이얼로그, 특수영역)
with tab_layouts:
    show_layout_tabs()

# 3. 데이터 표시 대분류 (표, 데이터프레임, 메트릭, JSON)
with tab_data:
    show_data_tabs()

# 4. 차트 & 시각화 대분류 (선/영역, 막대/산점도, 지도)
with tab_charts:
    show_chart_tabs()

# 5. 상태 & 알림 대분류 (메시지 상자, 진행률/로딩, 토스트/효과)
with tab_status:
    show_status_tabs()

# 6. 텍스트 & 서식 대분류 (타이포그래피, 마크다운/코드/수식)
with tab_text:
    show_text_tabs()

# 7. 미디어 대분류 (이미지, 오디오/비디오)
with tab_media:
    show_media_tabs()