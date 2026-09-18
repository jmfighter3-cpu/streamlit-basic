# 🎈 Streamlit Basic Showcase & AI Studio

Streamlit의 다양한 기본 위젯 및 레이아웃을 학습할 수 있는 종합 쇼케이스와, 최신 OpenAI API 및 SQLite 기반의 멀티모달 AI 대화형 챗봇 애플리케이션입니다.

---

## 🌟 프로젝트 특징

1. **🎨 Streamlit 기본 위젯 쇼케이스 (`app.py`)**
   - **입력 위젯**: 텍스트, 숫자, 슬라이더, 날짜/시간, 선택(드롭다운, 라디오 등)
   - **레이아웃**: 다단 컬럼, 컨테이너, 확장 패널(`expander`), 팝업 모달 다이얼로그(`@st.dialog`), 탭
   - **데이터 및 시각화**: 테이블, 데이터프레임, 메트릭 카드, 차트(선, 막대, 지도 등)
   - **상태 & 피드백**: 프로그레스 바, 스피너, 알림 배너, 토스트 알림, 축하 효과(`st.balloons`, `st.snow`)

2. **🧭 Google OAuth 인증 & 실무형 멀티페이지 네비게이션 (`app2.py`)**
   - **Google OIDC 로그인/로그아웃**: Streamlit 공식 인증(`st.login`, `st.logout`, `st.user`) 및 `.streamlit/secrets.toml` 연동
   - **동적 네비게이션 (`st.navigation`, `st.Page`)**: 로그인 상태에 따라 변화하는 사이드바 메뉴 (`Your account: [Log in/Log out, Settings]`, `Reports: [Overview]`)
   - **유기적 화면 전환**: `st.page_link`(빠른 바로가기 링크)와 `st.switch_page`(설정 저장 후 자동 대시보드 복귀)
   - **Streamlit Community Cloud 배포 진입점**

3. **🤖 멀티모달 AI Studio & 대화 보관함 (`app2-1.py`)**
   - **OpenAI 최신 모델 지원**: `gpt-5.6-luna` (기본), `gpt-5.6-terra`, `gpt-5.6-sol`, `gpt-5.5`
   - **멀티모달 기능**: 이미지(`jpg`, `png` 등) 및 문서 파일 분석 기능
   - **영구 보관 (SQLite)**: 대화 내역이 로컬 SQLite DB(`chat_history.db`)에 안전하게 저장 및 복원
   - **과거 대화 보관함**: `pages/app2_history.py` (또는 `app2-1_history.py`)

---

## 🚀 빠른 시작 가이드 (Quick Start)

### 1. 가상환경 및 패키지 설치 (`uv`)
본 프로젝트는 초고속 파이썬 패키지 매니저인 [`uv`](https://docs.astral.sh/uv/)를 사용합니다.

```bash
# uv 동기화 (가상환경 생성 및 필수 패키지 자동 설치)
uv sync
```

### 2. 애플리케이션 실행

- **1) Streamlit 기본 컴포넌트 쇼케이스 실행**:
  ```bash
  uv run streamlit run app.py
  # 또는 Windows 배치 파일: run.bat
  ```

- **2) Google 인증 & 멀티페이지 네비게이션 실행**:
  ```bash
  uv run python app2.py
  # 또는 Windows 배치 파일: run2.bat (또는 run3.bat)
  ```

- **3) 멀티모달 AI Studio 챗봇 실행**:
  ```bash
  uv run streamlit run app2-1.py
  # 또는 Windows 배치 파일: run2-1.bat
  ```

---

## 📁 프로젝트 폴더 구조

```text
streamlit-basic/
├── app.py                  # Streamlit 기초 위젯 종합 쇼케이스
├── app2.py                 # Google 인증 & 네비게이션 메인 진입점 (st.App)
├── stream_pages/           # 네비게이션 서브 페이지 (main, login, logout, dashboard, settings)
├── app2-1.py               # 멀티모달 AI 챗봇 메인 애플리케이션 (기존 app2.py)
├── pages/
│   └── app2_history.py     # AI 챗봇 과거 대화 내역 조회 및 통계/관리 페이지
├── widgets/                # 위젯 카테고리별 모듈화 코드
│   ├── inputs/             # 입력 컴포넌트
│   ├── layouts/            # 레이아웃 컴포넌트
│   ├── data/               # 데이터 표시 컴포넌트
│   ├── charts/             # 시각화 차트 컴포넌트
│   ├── status/             # 상태/알림 컴포넌트
│   ├── text/               # 텍스트/마크다운 컴포넌트
│   └── media/              # 미디어 컴포넌트
├── assets/                 # 이미지 및 미디어 리소스
├── .env.example            # 환경 변수 설정 템플릿
├── pyproject.toml          # 프로젝트 의존성 명세서
└── README.md               # 프로젝트 안내 문서
```

---

## 🛠️ 기술 스택 (Tech Stack)

- **언어**: Python 3.12+
- **패키지 관리자**: `uv`
- **웹 프레임워크**: `Streamlit`
- **AI API**: `OpenAI Python SDK` (Default: `gpt-5.6-luna`)
- **데이터베이스**: `SQLite3`, `Pandas`

