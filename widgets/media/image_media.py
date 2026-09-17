import streamlit as st

def show_image_media():
    """st.image를 활용한 이미지 출력 예시입니다."""
    st.subheader("이미지 표시 (st.image)")
    st.caption("로컬 파일 경로 또는 웹 URL의 이미지를 화면에 렌더링합니다.")

    # 로컬 이미지 파일 경로 지정 (assets 폴더 내 파일)
    local_image_path = "assets/sample_image.png"

    # st.image()로 로컬 이미지 출력
    st.image(
        local_image_path,
        caption="로컬 이미지 파일: assets/sample_image.png (st.image)",
        width="stretch"
    )
