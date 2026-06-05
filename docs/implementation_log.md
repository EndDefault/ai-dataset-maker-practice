# 구현 로그

구현한 내용과 이유를 날짜별로 기록한다.

## 2026-06-04 초기 방향 재정의

변경 내용:

- 프로젝트 방향을 로컬 AI 작업 비서로 다시 축소했다.
- 초기 기능 후보를 txt 파일 요약, 폴더 문서 검색, 에러 메시지 분석으로 좁혔다.
- docs 구조를 작게 다시 정의했다.
- Windows cmd 기준 명령어 규칙을 명시했다.
- 커밋 규칙은 계속 사용할 문서로 유지했다.

이유:

- OCR, RAG, LoRA, 번역 등 확장 기능을 한 번에 넣으면 범위가 너무 커진다.
- 먼저 완성 가능한 작업 수행형 AI 비서를 만드는 것이 목표다.

다음 작업:

- 기본 폴더 구조 생성
- Streamlit 앱 뼈대 생성
- 명령 분류 함수 구현
- txt 파일 요약 기능 구현

## 2026-06-06 로컬 실행 기준 재정리

변경 내용:

- 초기 구현 기능을 미리 확정하지 않기로 했다.
- 초기 후보 기능에 RAG 기반 문서 질의응답을 포함했다.
- RTX 5060 Ti 16GB 기준 모델 세트를 정했다.
- 메인 AI는 `qwen3:14b`, 입출력 정제 AI는 `qwen3:4b`, 임베딩 모델은 `bge-m3`로 둔다.
- SQLite 3.49.1 사용을 확인했다.
- `sqlite-vec`는 프로젝트 가상환경 `.venv`에 설치해서 검증하기로 했다.
- 고정 출력 파일명 대신 실행 ID 기반 파일명을 사용하기로 했다.
- 실패 상황은 오류 코드, Markdown 요약, 별도 `error.json`으로 남기기로 했다.
- LoRA는 처음부터 적용하지 않고, 입출력 정제 데이터가 쌓인 뒤 검토하기로 했다.
- Spring Boot는 장기 백엔드 후보로 두고, 현재는 SQLite 기반 로컬 구조를 우선한다.
- Streamlit UI는 Next.js식 `app/페이지명/page.py`와 `features/페이지명/` 구조를 참고해서 나누기로 했다.
- 커밋 메시지는 Gitmoji 기반 `<깃모지> <작업 분류> : <작업 내용>` 형식으로 정리했다.

이유:

- 기능을 먼저 확정하면 이후 RAG, DB, 입출력 구조 변경 때 문서와 구현이 쉽게 어긋난다.
- 로컬 단일 사용자 구조에서는 SQLite가 단순하고 운영 부담이 작다.
- 입출력 정제 AI와 schema 검증을 먼저 두면 메인 AI 출력 품질과 오류 처리 흐름을 안정화하기 쉽다.
- 페이지 조립과 페이지별 기능을 분리하면 UI가 커져도 구조를 찾기 쉽고, 나중에 React/Next.js로 옮길 때 개념을 유지하기 쉽다.

다음 작업:

- `sqlite-vec` 설치와 로드 테스트
- `requirements.txt` 생성
- 기본 폴더 구조 생성
- UI 폴더 구조 생성
- 작업 JSON schema 작성
- 입출력 정제 흐름 구현

## 2026-06-06 Streamlit 사이트 첫 버전 구현

변경 내용:

- `app.py` Streamlit 진입점을 만들었다.
- `src/ui/app`, `src/ui/features`, `src/ui/shared` 구조로 Home, Documents, Runs, Settings 페이지를 만들었다.
- 사용자 명령을 작업 JSON으로 바꾸는 기본 정규화와 schema 검증을 추가했다.
- 요약, 검색, 에러 분석, RAG 질의응답 후보 작업을 연결했다.
- Ollama 호출을 위한 `ollama_client.py`를 추가했다.
- Ollama가 느리거나 사용할 수 없을 때도 앱이 죽지 않도록 fallback 응답을 넣었다.
- SQLite 테이블 생성, 실행 기록, 산출물, 오류 기록 저장을 연결했다.
- Markdown 결과와 `error.json` 파일을 실행 ID 기준으로 저장한다.
- `requirements.txt`와 기본 디렉터리 `data`, `uploads`, `outputs`를 추가했다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- `streamlit --version` 확인: 1.58.0
- 앱 import와 SQLite 초기화 확인
- 로컬 실패 처리 경로 확인: `MISSING_FILE` 오류가 Markdown과 SQLite에 기록됨
- Streamlit 서버 응답 확인: `http://127.0.0.1:8501` HTTP 200

남은 작업:

- `sqlite-vec` 실제 로드 테스트와 벡터 검색 연결
- `bge-m3` embedding 저장
- `qwen3:4b` 기반 입출력 정제 AI 연결
- 기술 스택 입력 UI 보강
- Streamlit 화면 브라우저 시각 검증

## 2026-06-06 PDF 문서 입력 지원

변경 내용:

- 문서 로더가 `.pdf` 파일을 수집하도록 확장했다.
- `pypdf`를 사용해 텍스트 기반 PDF 내용을 추출한다.
- 업로드 UI와 문서 목록 안내 문구를 txt/md/pdf 기준으로 바꿨다.
- 요약, 검색, RAG 질의응답이 PDF 텍스트를 같은 chunk 흐름으로 사용할 수 있게 했다.

제한:

- 스캔 이미지 PDF는 아직 처리하지 않는다.
- 텍스트 추출이 되지 않는 PDF는 OCR 단계가 필요하다.
- PPT/PPTX는 아직 지원하지 않는다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- 임시 PDF 생성 후 `read_document_file()` 텍스트 추출 확인
- 지원 확장자 확인: `.txt`, `.md`, `.pdf`
- Streamlit 서버 응답 확인: `http://127.0.0.1:8501` HTTP 200
