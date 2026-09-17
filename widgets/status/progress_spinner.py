import streamlit as st
import time

def show_progress_spinner():
    """st.spinner, st.progress, st.status 예시입니다."""
    st.subheader("1. 로딩 스피너 (st.spinner)")
    st.caption("시간이 걸리는 작업을 처리할 때 회전 애니메이션과 안내 문구를 보여줍니다.")

    if st.button("스피너 테스트 실행"):
        with st.spinner("데이터를 불러오는 중입니다..."):
            time.sleep(1.5)
        st.success("데이터 로딩 완료!")

    st.divider()

    st.subheader("2. 진행률 표시 바 (st.progress)")
    st.caption("작업의 진행 상태를 0%에서 100%까지 게이지 바로 시각화합니다.")

    # 슬라이더로 진행률 바의 퍼센티지를 직접 조작해보기
    progress_val = st.slider("진행률 조절해보기 (%)", min_value=0, max_value=100, value=65)
    st.progress(progress_val)

    st.divider()

    st.subheader("3. 단계별 상태 컨테이너 (st.status)")
    st.caption("여러 단계의 긴 작업 흐름을 접었다 펼 수 있는 상태 컨테이너로 보여줍니다.")

    if st.button("단계별 작업 실행해보기"):
        with st.status("작업을 진행하고 있습니다...", expanded=True) as status:
            st.write("1단계: 환경 설정 점검...")
            time.sleep(0.8)
            st.write("2단계: 패키지 의존성 로딩...")
            time.sleep(0.8)
            st.write("3단계: 작업 마무리...")
            time.sleep(0.8)
            status.update(label="모든 작업이 성공적으로 완료되었습니다!", state="complete", expanded=False)

