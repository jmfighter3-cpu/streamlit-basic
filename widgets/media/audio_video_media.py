import streamlit as st

def show_audio_video_media():
    """st.audio와 st.video를 활용한 멀티미디어 재생 예시입니다."""
    st.subheader("1. 오디오 재생 (st.audio)")
    st.caption("웹 오디오 URL이나 사운드 파일을 내장 플레이어로 재생합니다.")

    # 공용 공개 오디오 샘플 URL
    sample_audio_url = "https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
    st.audio(sample_audio_url, format="audio/ogg")

    st.divider()

    st.subheader("2. 동영상 재생 (st.video)")
    st.caption("MP4 비디오 파일이나 유튜브(YouTube) 영상 링크를 직접 임베드하여 재생합니다.")

    # 공용 공개 비디오 샘플 URL
    sample_video_url = "https://www.w3schools.com/html/mov_bbb.mp4"
    st.video(sample_video_url)

