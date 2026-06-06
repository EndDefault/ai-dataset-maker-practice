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

현재 구현 상태는 `v0.3.3` 기준 복원 상태로 둔다.

`v0.3.3`은 item chunk 기반 RAG와 candidate_id 누락 보강을 유지한다.

`v0.3.4`의 section chunk 검색 실험은 제외 조건과 근거 세밀도에서 품질이 떨어져 현재 기준에서는 채택하지 않는다.

`v0.3.0`은 `v0.3.0` 태그로 저장한다.

다음 후보는 v0.3.3 기준 품질 평가표 작성, RAG 금액 추출 정확도 추가 관찰, `qwen3:4b` 기반 입출력 정제 AI 연결, OCR 지원이다.

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
- [x] 생성형 답변의 한국어 출력 안정화
- [x] 영어 응답으로 보이는 답변의 한국어 재작성 fallback 추가
- [x] 변경 없는 문서의 재분석 생략
- [x] Ollama 모델 설치 상태 확인: `qwen3:14b`, `qwen3:4b`, `bge-m3`
- [x] `bge-m3` embedding 1024차원 응답 확인
- [x] `sqlite-vec` `chunk_embeddings` 가상 테이블 연결
- [x] 문서 chunk embedding을 SQLite와 sqlite-vec에 저장
- [x] RAG 질의응답에서 벡터 검색을 우선 사용
- [x] 벡터 검색 실패 시 lexical fallback 검색으로 대체
- [x] Documents 페이지에 저장된 벡터 row 수 표시
- [x] RAG 검색 결과에 질문 핵심어 가중치 반영
- [x] RAG 답변에서 표 요청 시 Markdown 표 형식 강제
- [x] RAG 답변에서 허용된 근거 파일명만 사용하도록 프롬프트 강화
- [x] LLM 빈 응답 재시도 추가
- [x] 빈 결과 성공 처리 방지
- [x] 섹션 제목이 포함된 chunk와 다음 chunk를 우선 컨텍스트로 사용
- [x] 작업 지시어와 제외 지시어를 검색 핵심어에서 제거
- [x] 증액 금액은 `+N억원` 형식으로 정리하도록 프롬프트 강화
- [x] 문서 chunk에 `chunk_type`, `section_title`, `item_title`, `page_number`, `metadata_json` 저장
- [x] 섹션 질문에서 해당 섹션 item chunk 전체를 컨텍스트로 사용
- [x] candidate_id 기반 누락 후보 보강
- [x] Home 결과 미리보기에 이전 결과와 Streamlit 캐시 삭제 버튼 추가
- [x] v0.3.4 section chunk 검색 실험 결과를 보류
- [x] RAG/DB 검색 기준을 v0.3.3 item chunk 구조로 복원
- [x] Documents chunk 미리보기에서 section package 형태로 후보 항목 표시

## 진행 중

- [ ] v0.3.3 기준 RAG 품질 평가표 작성
- [ ] RAG 숫자 추출 후처리 검증 검토
- [ ] `qwen3:4b` 기반 입출력 정제 AI 연결

## 다음 작업

1. v0.3.3 기준으로 RAG 질문 5~10개를 평가한다.
2. `qwen3:4b` 기반 입출력 정제 AI 연결을 검토한다.
3. OCR 지원 범위와 우선순위를 정한다.
4. `v0.4.0` UI/UX 개편 후보를 정리한다.
