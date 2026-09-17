import streamlit as st
from .image_media import show_image_media
from .audio_video_media import show_audio_video_media

def show_media_tabs():
    """미디어(Media elements) 하위 탭들을 생성하고 각 화면을 연결합니다."""
    sub_tab1, sub_tab2 = st.tabs([
        "🖼️ 이미지 (Image)",
        "🎵 오디오 & 비디오 (Audio/Video)"
    ])

    with sub_tab1:
        show_image_media()

    with sub_tab2:
        show_audio_video_media()

