# 🤖 지능형 대학 생활 통합 가이드 시스템 — 단봇 (DAN-BOT)
---

## 프로젝트 소개

단국대학교 학생들을 위한 실시간 학사 정보 응대 및 스마트 캠퍼스 에이전트

매 학기 학생들은 수많은 학사 공지와 복잡한 규정 사이에서 자신에게 필요한 정보를 찾는 데 많은 시간을 사용합니다. 현재 단국대학교는 이러한 질의에 실시간으로 대응할 수 있는 전용 챗봇 시스템이 부재한 상황입니다.

**단봇(DAN-BOT)**은 이러한 불편함을 해소하기 위해 개발되었습니다. 본 프로젝트는 **로컬 LLM(Llama 3.2)**과 **실시간 웹 크롤링(Selenium)** 기술을 결합한 **RAG(Retrieval-Augmented Generation)** 아키텍처를 기반으로 하며, 학생들의 자연어 질문에 대해 학교 공식 데이터를 실시간으로 분석하여 가장 정확한 최신 정보를 제공합니다.

---

## 프로젝트 핵심 가치

1. **Zero-Delay Information**: 홈페이지 메뉴를 헤맬 필요 없이 단 한 번의 질문으로 원하는 정보에 도달합니다.

2. **Privacy-First AI**: Ollama 기반의 로컬 LLM을 운용하여 학생의 질의 데이터가 외부로 유출되지 않는 안전한 보안 환경을 제공합니다.

3. **Source Verifiability**: 모든 답변에 실제 학사 공지 링크를 매핑하여 AI의 답변을 사용자가 즉시 검증할 수 있습니다.

---

## 주요 기능

| 기능 | 상세 설명 |
|---|---|
| 자연어 의도 분석 | 사용자의 비정형 질의를 분석하여 학사/장학/시설 등의 카테고리로 자동 매핑 |
| 실시간 웹 스크래핑 | 질문 시점에 단국대 홈페이지에 즉시 접속하여 최신 공지 및 규정 데이터 추출 |
| 하이브리드 답변 생성 | 수집된 실시간 데이터와 LLM의 추론 능력을 결합한 요약 답변 생성 |
| 지능형 출처 매핑 | 답변의 근거가 되는 원문 URL을 자동으로 탐색하여 답변과 함께 제공 |
| 멀티미디어 가이드 | 캠퍼스 시설 및 위치 문의 시 시각적 이미지(맵) 동시 노출 |
| 퀵 메뉴 시스템 | 학사일정, 편의시설 등 빈도가 높은 질문을 원클릭으로 처리하는 UX 제공 |
| 로컬 AI 보안 | Ollama를 이용한 로컬 서버 운영으로 학생 질의 데이터 보안 유지 |
---

## 기술 스택

| Backend | 기술 |
|---|---|
| 프레임워크 | Flask (Python 3.12) |
| 데이터 수집 | Selenium WebDriver |
| 커뮤니케이션 | Real-time Data Streaming API |

| Frontend | 기술 |
|---|---|
| 인터페이스 | HTML / CSS / JS (Markdown-supported Chat UI) |
| 환경 관리 | Git, GitHub, venv |

| Artificial Intelligence | 기술 |
|---|---|
| AI 모델 | Ollama, Llama 3.2 (RAG 아키텍처 적용) |
| 방법론 | RAG / Context Injection |

---

## 시스템 아키텍쳐

단봇은 학생의 질문으로부터 답변까지 다음과 같은 RAG 프로세스를 거칩니다.

```
사용자 질문      # 사용자가 대화창을 통해 자연어 질문 입력
    ↓
의도 분석      # Flask 서버에서 질문의 키워드 및 의도 분석
    ↓
실시간 검색      # Selenium이 타겟 페이지에 접속하여 최신 학사 데이터 수집
    ↓
AI 추론      # 수집된 데이터를 Llama 3.2 모델에 주입(Context Injection)하여 답변 생성
    ↓
최종 응답      # 요약 답변, 관련 이미지, 원문 링크를 사용자에게 최종 출력
```

---

## 개발 로드맵

# Phase 1: Foundation (W1 - W4)

- 요구사항 정의 및 시스템 아키텍처 설계
- Selenium 기반 동적 웹 크롤링 엔진 및 예외 처리 시스템 구축

# Phase 2: Intelligence (W5 - W7)

- Ollama 서빙 및 RAG 로직 최적화 (프롬프트 엔지니어링)
- Flask 기반 백엔드 API와 프론트엔드 채팅 UI 연동

# Phase 3: Optimization (W8 - W10)

- 데이터 정합성 검증 및 할루시네이션(환각) 방지 필터링 테스트
- 베타 테스트 피드백 반영 및 최종 문서화

---

## 팀원

| 이름 | 역할 | 
|---|---|
| 임찬형 | 전체 시스템 설계, Flask 서버 구축 및 모듈 통합 관리 |
| 김희수 | 실시간 크롤링 엔진 구축 및 데이터 정제 알고리즘 구현 |
| 정지윤 | Ollama 모델 최적화 및 RAG 시스템 아키텍처 설계 |
| 주예나 | 웹 UI 개발, 시각 자산 관리 및 기술 문서화 |
---

## 실행 가이드

```bash
# 1. 레포지토리 클론
git clone https://github.com/Your-Repo/DAN-BOT.git

# 2. 가상환경 설정 및 패키지 설치
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. 로컬 AI 모델 실행 (Ollama 필요)
ollama run llama3.2

# 4. 서버 구동
python src/app.py
```

---

## 프로젝트 구조

```
dan-bot/
├── assets/               # README용 이미지, 로고, UML 다이어그램
├── docs/                 # 설계 문서
│   ├── UserGuide.md      # 사용자 매뉴얼
│   └── DeveloperGuide.md # 시스템 설계 및 API 명세서
├── src/                  # 메인 소스 코드 디렉토리
│   ├── crawler/          # Selenium 기반 웹 스크래핑 모듈
│   │   ├── __init__.py
│   │   └── scraper.py    # 단국대 홈페이지 동적 파싱 로직
│   ├── ai_engine/        # Ollama 및 LLM 연동 모듈
│   │   ├── __init__.py
│   │   ├── llm_handler.py# Llama 3.2 모델 호출 및 프롬프트 제어
│   │   └── rag_logic.py  # 컨텍스트 주입 및 데이터 요약 로직
│   ├── static/           # 프론트엔드 정적 파일 (CSS, JS, 로컬 이미지)
│   │   ├── css/          # 채팅 UI 스타일시트
│   │   └── js/           # 비동기 통신 및 DOM 조작 스크립트
│   ├── templates/        # Flask HTML 템플릿
│   │   └── index.html    # 메인 채팅 인터페이스
│   └── app.py            # Flask 메인 서버 실행 파일
├── tests/                # 유닛 테스트 및 성능 검증 코드
├── .gitignore            # Git 관리 제외 대상 (venv, .env, pycache 등)
├── README.md             # 프로젝트 메인 소개 및 가이드
└── requirements.txt      # 프로젝트 의존성 라이브러리 목록
```
---
