import streamlit as st
import datetime

def show_datetime_widgets():
    """날짜, 시간, 색상 선택 관련 위젯들을 화면에 표시합니다."""
    st.subheader("1. 날짜 입력 (st.date_input)")

    # (1) 단일 날짜 선택
    # - value: 기본 선택 날짜 (오늘 날짜)
    today = datetime.date.today()
    selected_date = st.date_input(label="예약 날짜 선택", value=today)
    st.write(f"👉 선택한 날짜: **{selected_date}**")

    # (2) 기간(시작일 ~ 종료일) 선택
    # - value에 (시작일, 종료일) 튜플을 전달하면 기간 범위 선택 모드가 됩니다.
    next_week = today + datetime.timedelta(days=7)
    date_range = st.date_input(
        label="여행 기간 선택 (시작일 ~ 종료일)",
        value=(today, next_week)
    )
    st.write(f"👉 선택한 기간: **{date_range}**")

    st.divider()

    st.subheader("2. 시간 입력 (st.time_input)")
    # - value: 기본 시간 (시, 분)
    alarm_time = st.time_input(
        label="알람 시간 설정",
        value=datetime.time(8, 30)
    )
    st.write(f"👉 설정된 시간: **{alarm_time}**")

    st.divider()

    st.subheader("3. 색상 선택기 (st.color_picker)")
    # - value: 기본 색상 코드
    picked_color = st.color_picker(
        label="원하는 색상을 골라보세요",
        value="#00f900"
    )
    st.write(f"👉 선택한 색상 코드: **{picked_color}**")

