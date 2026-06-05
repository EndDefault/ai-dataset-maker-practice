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
- [ ] 기본 폴더 구조 생성
- [x] `.gitignore`에 `.venv/`, `outputs/`, `data/*.db` 정리

## Phase 2. 로컬 실행 환경

- [ ] `.venv` 활성화 확인
- [ ] `sqlite-vec` 설치
- [ ] `sqlite-vec` 로드 테스트
- [ ] `requirements.txt` 생성
- [ ] Ollama 모델 확인: `qwen3:14b`, `qwen3:4b`, `bge-m3`

## Phase 3. 입출력 정제

- [ ] Streamlit 명령 입력창
- [ ] 작업 JSON schema 작성
- [ ] `qwen3:4b` 기반 입력 정제 함수
- [ ] JSON 검증 실패 처리
- [ ] 알 수 없는 명령 fallback 안내

## Phase 3-1. UI 뼈대

- [ ] `src/ui/app/home/page.py` 생성
- [ ] `src/ui/app/documents/page.py` 생성
- [ ] `src/ui/app/runs/page.py` 생성
- [ ] `src/ui/app/settings/page.py` 생성
- [ ] `src/ui/features/home/` 생성
- [ ] `src/ui/features/documents/` 생성
- [ ] `src/ui/features/runs/` 생성
- [ ] `src/ui/features/settings/` 생성
- [ ] `src/ui/shared/` 공통 컴포넌트 생성
- [ ] Streamlit navigation 연결

## Phase 4. 저장과 RAG 기반

- [ ] `data/app.db` 생성
- [ ] `runs` 테이블 생성
- [ ] `documents` 테이블 생성
- [ ] `chunks` 테이블 생성
- [ ] `artifacts` 테이블 생성
- [ ] `errors` 테이블 생성
- [ ] 문서 chunk 분리
- [ ] `bge-m3` embedding 생성
- [ ] SQLite 벡터 검색 검증

## Phase 5. 후보 기능 구현

- [ ] 요약 함수 연결
- [ ] 검색 함수 연결
- [ ] 에러 분석 함수 연결
- [ ] RAG 질의응답 함수 연결
- [ ] 알 수 없는 명령 안내

## Phase 6. txt/md 파일 요약 후보

- [ ] uploads 폴더 생성
- [ ] txt/md 파일 읽기
- [ ] `qwen3:14b`에 요약 요청
- [ ] 요약 결과 출력
- [ ] 실행 ID 기준 Markdown 저장

## Phase 7. 파일 검색 후보

- [ ] txt/md 파일 탐색
- [ ] 키워드 추출
- [ ] 관련 문단 검색
- [ ] 검색 결과 정리
- [ ] Markdown 저장

## Phase 8. 에러 메시지 분석 후보

- [ ] 에러 메시지 입력
- [ ] 기술 스택 입력
- [ ] 에러 의미 설명
- [ ] 원인과 해결 방법 출력
- [ ] Markdown 저장

## Phase 9. 실패 처리와 정리

- [ ] 오류 코드 정의
- [ ] 실패 Markdown 저장
- [ ] `error.json` 저장
- [ ] SQLite 오류 기록 저장
- [ ] 입출력 예시 문서화
- [ ] README 실행 방법 갱신
- [ ] implementation_log 갱신
- [ ] 테스트 결과 기록
