import streamlit as st

def show_text_widgets():
    """텍스트 입력 관련 위젯들을 화면에 표시합니다."""
    st.subheader("1. 한 줄 텍스트 입력 (st.text_input)")

    # (1) 기본 텍스트 입력
    # - label: 입력창 위에 표시할 제목
    # - value: 입력창에 미리 채워둘 기본값
    name = st.text_input(label="이름", value="홍길동")
    st.write(f"👉 입력된 이름: **{name}**")

    # (2) 안내 문구(placeholder)와 도움말(help)
    # - placeholder: 입력창이 비었을 때 보이는 힌트 문구
    # - help: 물음표 아이콘에 마우스를 올리면 나타나는 설명 툴팁
    email = st.text_input(
        label="이메일 주소",
        placeholder="example@email.com",
        help="안내 메일을 받을 이메일 주소를 입력하세요."
    )
    st.write(f"👉 입력된 이메일: **{email}**")

    # (3) 비밀번호 입력 (마스킹)
    # - type="password": 입력 글자를 가려주는 보안 모드
    password = st.text_input(label="비밀번호", type="password")
    st.write(f"👉 입력된 비밀번호: **{password}**")

    # (4) 글자 수 제한 (max_chars)
    # - max_chars: 입력 가능한 최대 글자 수
    nickname = st.text_input(label="닉네임 (최대 6글자)", max_chars=6)
    st.write(f"👉 입력된 닉네임: **{nickname}**")

    # (5) 비활성화 (disabled)
    # - disabled=True: 읽기 전용 상태로 잠금
    st.text_input(
        label="수정 불가 항목",
        value="이 항목은 비활성화되어 수정할 수 없습니다.",
        disabled=True
    )

    st.divider()

    st.subheader("2. 여러 줄 텍스트 입력 (st.text_area)")
    # st.text_area()는 긴 문장이나 메모를 여러 줄로 입력받을 때 사용합니다.
    # - height: 입력창 세로 높이 (픽셀 단위)
    # - max_chars: 최대 글자 수
    memo = st.text_area(
        label="자기소개 또는 메모",
        placeholder="자유롭게 긴 글을 입력해 보세요.",
        height=120,
        max_chars=200
    )
    st.write("👉 작성된 내용:")
    st.write(memo)

