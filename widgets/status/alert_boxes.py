import streamlit as st

def show_alert_boxes():
    """상태 알림 상자(success, info, warning, error) 예시입니다."""
    st.subheader("상태 알림 메시지 상자")
    st.caption("사용자에게 처리 결과, 안내, 경고, 에러 등을 색상별 상자로 명확히 알립니다.")

    st.success("✅ 성공 (st.success): 데이터 저장이 안전하게 완료되었습니다.")
    st.info("ℹ️ 안내 (st.info): 새로운 기능이 업데이트되었습니다.")
    st.warning("⚠️ 경고 (st.warning): 남은 사용 기한이 3일 남았습니다.")
    st.error("❌ 에러 (st.error): 네트워크 연결이 원활하지 않습니다.")

