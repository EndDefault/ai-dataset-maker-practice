# 현재 상태

## 한 문장 요약

로컬 LLM, SQLite, RAG 기반을 이용해 파일 작업을 수행하고 결과를 Markdown으로 저장하는 로컬 AI 작업 비서를 만든다.

## 현재 목표

- 자연어 명령을 입력받는다.
- 입출력 정제 AI가 명령을 작업 JSON으로 변환한다.
- 코드가 JSON schema를 검증한 뒤 작업별 Python 함수를 실행한다.
- 메인 AI는 최종 답변, 요약, 에러 분석 설명 생성을 맡는다.
- RAG가 필요한 경우 `bge-m3`와 SQLite 벡터 검색을 사용한다.
- 결과, 실행 기록, 오류 정보를 Markdown과 SQLite에 저장한다.

## 현재 버전

현재 구현 상태는 `v0.2.0`으로 둔다.

`v0.2.0`은 Streamlit 기반 로컬 AI 작업 콘솔에 문서 처리 상태 확인 기능을 추가한 버전이다.

다음 버전은 `v0.3.0`이며, OCR 또는 실제 embedding/RAG 연결 중 우선순위가 높은 기능을 진행한다.

## 완료된 것

- [x] 프로젝트 방향을 로컬 AI 작업 비서로 축소
- [x] 초기 구현 기능 고정 방침 제거
- [x] 초기 기능 후보 정리
- [x] docs 구조 단순화
- [x] Windows cmd 기준 명령어 규칙 명시
- [x] Gitmoji 커밋 규칙 정리
- [x] RTX 5060 Ti 16GB 기준 모델 세트 결정
- [x] SQLite 3.49.1 사용 확인
- [x] Python 가상환경 사용 방침 결정
- [x] Streamlit UI 구조 초안 결정
- [x] Next.js식 `app/페이지명/page.py`와 `features/페이지명/` 구조 반영
- [x] Streamlit 사이트 첫 버전 구현
- [x] SQLite 실행 기록과 Markdown/error 파일 저장 연결
- [x] Home, Documents, Runs, Settings 페이지 생성
- [x] `sqlite-vec` 로드 테스트 확인
- [x] 문서별 인덱싱 상태 표시
- [x] PDF 텍스트 추출 가능 여부와 스캔 PDF 추정 표시
- [x] 문서별 PDF 페이지 수, 추출 글자 수, 청크 수 표시
- [x] 문서 분석 결과를 SQLite `documents`, `chunks` 테이블에 저장
- [x] 인덱싱 상태가 좋지 않은 문서를 Home에서 실행 전에 경고

## 진행 중

- [ ] SQLite와 `sqlite-vec` 실제 벡터 검색 연결
- [ ] `qwen3:4b` 기반 입출력 정제 AI 연결
- [ ] `bge-m3` 기반 embedding 생성과 벡터 검색 연결

## 다음 작업

1. Ollama 모델 설치 상태를 확인한다: `qwen3:14b`, `qwen3:4b`, `bge-m3`.
2. `bge-m3` embedding 생성과 SQLite 저장 흐름을 연결한다.
3. `sqlite-vec` 실제 벡터 검색을 검증한다.
4. `qwen3:4b` 기반 입출력 정제 AI를 연결한다.
5. OCR과 실제 RAG 연결 중 `v0.3.0` 우선순위를 확정한다.
