import streamlit as st

def show_metric_widgets():
    """st.metric을 활용한 핵심 지표 카드 표시 예시입니다."""
    st.subheader("핵심 성과 지표 (st.metric)")
    st.caption("대시보드에서 매출, 사용자 수, 온도 등의 주요 수치와 증감을 한눈에 보여줍니다.")

    # 3개 컬럼으로 지표 나란히 배치
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="오늘 방문자 수",
            value="1,250명",
            delta="150명 (12%)"  # 양수 증가는 초록색 화살표
        )

    with col2:
        st.metric(
            label="월간 매출액",
            value="45,000,000원",
            delta="-2,500,000원",  # 음수 감소는 빨간색 화살표
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="서버 응답 속도",
            value="42ms",
            delta="-15ms",
            delta_color="inverse"  # 속도 감소는 좋은 것이므로 색상 반전 가능
        )

