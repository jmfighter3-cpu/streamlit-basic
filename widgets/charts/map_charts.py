import streamlit as st
import pandas as pd

def show_map_charts():
    """st.map을 활용한 인터랙티브 지도 시각화 예시입니다."""
    st.subheader("지도 시각화 (st.map)")
    st.caption("위도(lat)와 경도(lon) 데이터를 전달하면 지도 위에 지점을 표시해줍니다.")

    # 서울 주요 거점 좌표 데이터
    locations = pd.DataFrame({
        "lat": [37.5665, 37.5512, 37.4979, 37.5133],
        "lon": [126.9780, 126.9882, 127.0276, 127.1001]
    })

    # 지도 표시 (zoom 파라미터로 확대 수준 지정 가능)
    st.map(locations, zoom=11)

