import streamlit as st

def show_number_slider_widgets():
    """숫자 입력 및 슬라이더 관련 위젯들을 화면에 표시합니다."""
    st.subheader("1. 숫자 입력 (st.number_input)")

    # (1) 정수 입력 - 예: 수량
    # - min_value: 최솟값
    # - max_value: 최댓값
    # - step: 증감 단위
    quantity = st.number_input(
        label="주문 수량 선택 (개)",
        min_value=1,
        max_value=100,
        value=1,
        step=1
    )
    st.write(f"👉 선택한 수량: **{quantity}개**")

    # (2) 소수점(실수) 입력 - 예: 신장(키)
    # - format: 소수점 자릿수 포맷
    height = st.number_input(
        label="키 입력 (cm)",
        min_value=100.0,
        max_value=250.0,
        value=175.5,
        step=0.5,
        format="%.1f"
    )
    st.write(f"👉 입력한 키: **{height}cm**")

    st.divider()

    st.subheader("2. 슬라이더 (st.slider)")

    # (1) 단일 값 슬라이더
    age = st.slider(
        label="나이 선택",
        min_value=1,
        max_value=100,
        value=25,
        step=1
    )
    st.write(f"👉 선택한 나이: **{age}세**")

    # (2) 구간 범위(Range) 슬라이더
    # - value에 (최소, 최대) 튜플을 넘겨주면 범위 선택 슬라이더가 됩니다.
    score_range = st.slider(
        label="시험 점수 구간 선택",
        min_value=0,
        max_value=100,
        value=(30, 80)
    )
    st.write(f"👉 선택한 점수 구간: **{score_range[0]}점 ~ {score_range[1]}점**")

