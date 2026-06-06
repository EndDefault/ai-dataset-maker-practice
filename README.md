# Local AI Task Assistant

클라우드 API 비용 부담 없이 로컬 환경에서 동작하는 작업 수행형 AI 비서다.

사용자가 자연어로 명령을 입력하면 AI 비서가 명령 의도를 파악하고, 문서 요약, 파일 검색, 코드 오류 분석 같은 반복 작업을 수행한 뒤 결과를 보기 쉬운 Markdown 형태로 제공한다.

## 현재 단계

이 저장소는 docs-first 방식으로 진행한다.

현재 구현 상태는 `v0.2.1`이다.

`v0.2.1`은 Streamlit 기반 로컬 작업 콘솔에 문서 처리 상태 확인, 한국어 출력 안정화, 변경 없는 문서 재분석 생략을 추가한 버전이다.

현재 지원 기능:

- txt/md/pdf 문서 요약
- txt/md/pdf 문서 검색
- 에러 메시지 분석
- RAG 기반 문서 질의응답 후보 기능
- 문서별 인덱싱 상태, PDF 페이지 수, 추출 글자 수, chunk 수 표시
- 영어 응답으로 보이는 생성형 답변의 한국어 재작성 fallback

## 현재 합의된 로컬 기준

- GPU 기준: RTX 5060 Ti 16GB
- 메인 응답 모델: `qwen3:14b`
- 입출력 정제 모델: `qwen3:4b`
- 임베딩 모델: `bge-m3`
- DB: SQLite
- 벡터 검색 후보: `sqlite-vec`
- Python 실행: 프로젝트 가상환경 `.venv`

## 중요한 개발 규칙

이 프로젝트의 명령어와 문서는 **Windows cmd 기준**으로 작성한다.

PowerShell 전용 명령어를 기본 실행 방법으로 쓰지 않는다.

## 문서

시작점은 [docs/index.md](docs/index.md)다.

## 실행 방법

Windows `cmd` 기준:

```cmd
.venv\Scripts\activate
streamlit run app.py
```

브라우저에서 아래 주소를 연다.

```txt
http://127.0.0.1:8501
```

현재 사이트는 Streamlit 작업 콘솔이다.

- Home: 자연어 명령 실행과 Markdown 결과 미리보기
- Documents: txt/md/pdf 업로드, 문서 상태, PDF 페이지 수, 추출 글자 수, chunk 수, chunk 미리보기
- Runs: 실행 기록, Markdown 산출물, error.json 확인
- Settings: Ollama 모델, SQLite DB, 경로 상태 확인

## 현재 RAG 상태

현재 RAG 질의응답은 문서를 chunk로 나눈 뒤 lexical fallback 검색을 사용한다.

`bge-m3` embedding과 `sqlite-vec` 실제 벡터 검색 연결은 다음 단계인 `v0.3.0` 후보로 둔다.

질문은 문서 안에 직접 나올 법한 키워드를 포함하면 더 잘 동작한다.

예시:

```txt
2026년 예산안 자료를 기준으로 저출생, 보육, 청년 지원과 관련된 예산 항목을 찾아서 항목별 지원 내용과 금액을 표로 정리해줘. 근거가 된 파일명도 함께 표시해줘.
```
