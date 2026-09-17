import streamlit as st

def show_json_dict():
    """st.json을 활용한 JSON 데이터 계층 구조 표시 예시입니다."""
    st.subheader("JSON 데이터 뷰어 (st.json)")
    st.caption("파이썬 딕셔너리나 JSON 객체를 클릭하여 접고 펼칠 수 있는 인터랙티브 트리로 보여줍니다.")

    user_profile = {
        "user_id": 1001,
        "name": "홍길동",
        "is_active": True,
        "contact": {
            "email": "gildong@example.com",
            "phone": "010-1234-5678"
        },
        "skills": ["Python", "Streamlit", "Data Science"],
        "preferences": {
            "theme": "dark",
            "notifications": {
                "email": True,
                "sms": False
            }
        }
    }

    # st.json()으로 출력 (expanded=True로 기본 펼침 상태 지정 가능)
    st.json(user_profile, expanded=True)

