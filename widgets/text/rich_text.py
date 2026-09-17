import streamlit as st

def show_rich_text():
    """st.markdown, st.code, st.latex 예시입니다."""
    st.subheader("1. 마크다운 (st.markdown)")
    st.caption("굵은 글씨, 기울임, 컬러 텍스트, 링크, 이모지 등을 자유롭게 표현합니다.")

    st.markdown("""
    * **굵은 텍스트** 및 *기울임 텍스트*
    * Streamlit 컬러 텍스트 지원: :blue[파란색 텍스트], :red[빨간색 텍스트], :green[초록색 텍스트]
    * 이모지 표현: :sparkles: :rocket: :fire:
    """)

    st.divider()

    st.subheader("2. 코드 블록 (st.code)")
    st.caption("프로그래밍 언어 문법 하이라이팅과 우측 상단 복사(Copy) 버튼을 지원합니다.")

    sample_python_code = """def hello_streamlit():
    message = "Streamlit은 정말 직관적입니다!"
    print(message)
    return message
"""
    st.code(sample_python_code, language="python")

    st.divider()

    st.subheader("3. 수학 공식 (st.latex)")
    st.caption("LaTeX 문법을 사용하여 수학, 과학 공식을 미려하게 렌더링합니다.")

    st.latex(r"""
    E = mc^2 \quad \text{또는} \quad f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}
    """)

