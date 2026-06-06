# 체크리스트

## Phase 1. 프로젝트 기초

- [x] 프로젝트 방향 축소
- [x] 고정 초기 기능 제거
- [x] 초기 기능 후보 정리
- [x] docs 단순화
- [x] cmd 기준 명령어 규칙 작성
- [x] RTX 5060 Ti 16GB 기준 모델 세트 결정
- [x] SQLite 3.49.1 확인
- [x] Python 가상환경 사용 방침 결정
- [x] Streamlit UI 구조 초안 결정
- [x] Next.js식 UI 폴더 구조 반영
- [x] 기본 폴더 구조 생성
- [x] `.gitignore`에 `.venv/`, `outputs/`, `data/*.db` 정리

## Phase 2. 로컬 실행 환경

- [x] `.venv` 활성화 확인
- [x] `sqlite-vec` 설치
- [x] `sqlite-vec` 로드 테스트
- [x] `requirements.txt` 생성
- [x] Ollama 모델 확인: `qwen3:14b`, `qwen3:4b`, `bge-m3`

## Phase 3. 입출력 정제

- [x] Streamlit 명령 입력창
- [x] 작업 JSON schema 작성
- [ ] `qwen3:4b` 기반 입력 정제 함수
- [x] JSON 검증 실패 처리
- [x] 알 수 없는 명령 fallback 안내

## Phase 3-1. UI 뼈대

- [x] `src/ui/app/home/page.py` 생성
- [x] `src/ui/app/documents/page.py` 생성
- [x] `src/ui/app/runs/page.py` 생성
- [x] `src/ui/app/settings/page.py` 생성
- [x] `src/ui/features/home/` 생성
- [x] `src/ui/features/documents/` 생성
- [x] `src/ui/features/runs/` 생성
- [x] `src/ui/features/settings/` 생성
- [x] `src/ui/shared/` 공통 컴포넌트 생성
- [x] Streamlit navigation 연결

## Phase 4. 저장과 RAG 기반

- [x] `data/app.db` 생성
- [x] `runs` 테이블 생성
- [x] `documents` 테이블 생성
- [x] `chunks` 테이블 생성
- [x] `artifacts` 테이블 생성
- [x] `errors` 테이블 생성
- [x] 문서 chunk 분리
- [x] `bge-m3` embedding 생성
- [x] SQLite 벡터 검색 검증

## Phase 5. 후보 기능 구현

- [x] 요약 함수 연결
- [x] 검색 함수 연결
- [x] 에러 분석 함수 연결
- [x] RAG 질의응답 함수 연결
- [x] 알 수 없는 명령 안내

## Phase 6. txt/md/pdf 파일 요약 후보

- [x] uploads 폴더 생성
- [x] txt/md/pdf 파일 읽기
- [x] PDF 텍스트 추출
- [x] `qwen3:14b`에 요약 요청
- [x] 요약 결과 출력
- [x] 실행 ID 기준 Markdown 저장

## Phase 7. 파일 검색 후보

- [x] txt/md/pdf 파일 탐색
- [ ] 키워드 추출
- [x] 관련 문단 검색
- [x] 검색 결과 정리
- [x] Markdown 저장

## Phase 8. 에러 메시지 분석 후보

- [x] 에러 메시지 입력
- [ ] 기술 스택 입력
- [x] 에러 의미 설명
- [x] 원인과 해결 방법 출력
- [x] Markdown 저장

## Phase 9. 실패 처리와 정리

- [x] 오류 코드 정의
- [x] 실패 Markdown 저장
- [x] `error.json` 저장
- [x] SQLite 오류 기록 저장
- [ ] 입출력 예시 문서화
- [x] README 실행 방법 갱신
- [x] implementation_log 갱신
- [x] 테스트 결과 기록

## Phase 10. v0.2.0 문서 처리 상태

- [x] 문서 상태 값 정의: 업로드됨, 인덱싱 완료, 텍스트 없음, 스캔 PDF 추정, 지원하지 않는 파일, 오류
- [x] PDF 페이지 수와 텍스트 추출 가능 여부 확인
- [x] 스캔 PDF 추정 상태 표시
- [x] 문서별 추출 글자 수 표시
- [x] 문서별 청크 수 표시
- [x] 문서 처리 오류 메시지 저장
- [x] SQLite `documents` 테이블에 문서 분석 메타데이터 저장
- [x] SQLite `chunks` 테이블을 문서 분석 결과와 동기화
- [x] Documents 페이지에 문서 상태와 처리 정보 표시
- [x] Home 페이지에서 상태가 좋지 않은 입력 문서 경고

## Phase 11. v0.2.1 사용성 개선

- [x] 생성형 답변 기본 system prompt를 한국어 기준으로 설정
- [x] 영어 응답 감지 함수 추가
- [x] 영어 응답의 한국어 재작성 fallback 추가
- [x] 요약, RAG 질의응답, 에러 분석에 한국어 출력 안정화 연결
- [x] 변경 없는 문서 재분석 생략
- [x] 문서 재분석 생략 동작 확인

## Phase 12. v0.3.0 실제 벡터 RAG 연결

- [x] `bge-m3` 실제 embedding 응답 확인
- [x] 기본 embedding 차원 1024 설정
- [x] `sqlite-vec` `chunk_embeddings` 가상 테이블 생성
- [x] chunk embedding을 `embeddings` 메타 테이블과 `chunk_embeddings` 벡터 테이블에 저장
- [x] 문서 재분석과 삭제 시 기존 embedding row 정리
- [x] RAG 질의응답에서 벡터 검색을 우선 사용
- [x] 벡터 검색 실패 시 lexical fallback 검색 사용
- [x] RAG sources에 `search_mode` 기록
- [x] Documents 페이지에 저장된 벡터 row 수 표시
