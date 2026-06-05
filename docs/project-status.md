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

## 진행 중

- [ ] 기본 폴더 구조 결정
- [ ] SQLite와 `sqlite-vec` 사용 방식 검증
- [ ] 입출력 작업 JSON schema 결정

## 다음 작업

1. `.venv` 기준으로 `sqlite-vec` 설치와 로드 테스트를 한다.
2. `requirements.txt`를 만든다.
3. `architecture.md` 기준으로 기본 폴더 구조와 UI 폴더 구조를 만든다.
4. 작업 JSON schema와 입출력 정제 흐름을 먼저 구현한다.
5. 이후 후보 기능 중 가장 작은 작업부터 구현한다.
