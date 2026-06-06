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

## 2026-06-06 입력 파일 선택 UX 개선

변경 내용:

- Home의 직접 입력 경로 칸을 업로드 파일 선택 방식으로 바꿨다.
- 사용자는 업로드된 파일을 하나씩 추가해서 이번 작업 입력 목록을 만든다.
- 선택한 입력 파일은 실행 전 삭제할 수 있다.
- 입력 파일을 선택하지 않으면 작업을 실행하지 않고 안내한다.
- Documents 문서 목록에서 업로드 파일을 삭제할 수 있게 했다.
- 문서 삭제 시 SQLite 문서 기록과 Home 입력 목록에서도 함께 제거한다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- SQLite 초기화 확인
- Streamlit 서버 응답 확인: `http://127.0.0.1:8501` HTTP 200

## 2026-06-06 버전 계획 정리

변경 내용:

- 현재 구현 상태를 `v0.1.0`으로 정의했다.
- 다음 업데이트를 `v0.2.0`으로 두고, 문서 인덱싱 상태 표시를 중심 목표로 정했다.
- `v0.2.0`에서는 문서별 상태, PDF 텍스트 추출 여부, 스캔 PDF 추정, 추출 글자 수, 청크 수를 보여주기로 했다.
- 큰 UI/UX 개편은 기능 흐름이 더 잡힌 뒤 `v0.4.0` 전후에 진행하는 것으로 정했다.

이유:

- 지금 버전은 첫 사용 가능 버전이지만, 아직 OCR과 실제 벡터 RAG가 연결되지 않았다.
- 다음 단계에서는 기능을 무리하게 늘리기보다 사용자가 업로드 문서의 처리 상태를 신뢰할 수 있게 만드는 것이 우선이다.
- UI를 너무 일찍 크게 바꾸면 문서 상태, OCR, RAG 흐름이 추가될 때 다시 수정해야 할 가능성이 높다.

## 2026-06-06 v0.2.0 문서 처리 상태 구현

변경 내용:

- 문서 상태 값을 정의했다: 업로드됨, 인덱싱 완료, 텍스트 없음, 스캔 PDF 추정, 지원하지 않는 파일, 오류.
- PDF 분석에서 페이지 수, 텍스트 추출 페이지 수, 추출 텍스트를 함께 계산하도록 분리했다.
- 문서별 추출 글자 수와 chunk 수를 계산한다.
- `documents` 테이블에 `file_type`, `status`, `page_count`, `extracted_char_count`, `chunk_count`, `text_extractable`, `is_scanned_pdf`, `error_message`, `analyzed_at` 컬럼을 추가했다.
- 기존 DB도 새 컬럼을 받을 수 있도록 `initialize_database()`에서 문서 테이블 업그레이드를 수행한다.
- 문서 분석 결과에 맞춰 `chunks` 테이블을 다시 동기화한다.
- Documents 페이지에서 문서 상태, PDF 페이지 수, 추출 글자 수, chunk 수, 마지막 분석 시각을 보여준다.
- chunk 미리보기는 텍스트 없는 문서나 스캔 PDF 추정 문서를 예외 대신 경고로 안내한다.
- Home 페이지에서 선택한 입력 문서의 상태와 추출 글자 수, chunk 수를 보여주고, 상태가 좋지 않은 문서를 실행 전에 경고한다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- `initialize_database()` 실행 후 새 `documents` 컬럼 생성 확인
- uploads 폴더 문서 4개 분석 확인
- 분석 결과 예시: PDF 3개와 md 1개 모두 `indexed` 상태로 저장
- `chunks` 테이블 총 18개 chunk 저장 확인

남은 작업:

- `bge-m3` embedding 생성과 저장 연결
- `sqlite-vec` 실제 벡터 검색 검증
- `qwen3:4b` 기반 입출력 정제 AI 연결
- OCR 또는 실제 RAG 연결 중 `v0.3.0` 우선순위 확정

## 2026-06-06 v0.2.1 사용성 개선

변경 내용:

- 생성형 답변의 기본 system prompt를 한국어 작업 비서 기준으로 설정했다.
- 요약, RAG 질의응답, 에러 분석 작업에서 `generate_korean()`을 사용하도록 바꿨다.
- 긴 영어 응답으로 보이는 결과는 한국어 Markdown으로 한 번 재작성하는 fallback을 추가했다.
- 파일 크기와 수정 시간이 바뀌지 않은 문서는 `upsert_document()`에서 재분석하지 않도록 했다.
- Home과 Documents 페이지 렌더링 중 같은 PDF를 반복 분석하는 비용을 줄였다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- 긴 영어 응답은 한국어 재작성 대상으로 감지되고, 한국어 응답은 재작성하지 않는지 확인
- 같은 문서를 두 번 `upsert_document()`했을 때 `analyzed_at` 값이 유지되는지 확인

남은 작업:

- 실제 요약 실행에서 한국어 재작성 fallback이 필요한 빈도를 관찰한다.
- 반복되는 입출력 패턴이 쌓이면 LoRA 학습 데이터로 활용할 수 있는 저장 구조를 검토한다.
- `bge-m3` embedding 생성과 `sqlite-vec` 실제 검색 연결을 다음 후보로 유지한다.

## 2026-06-06 v0.3.0 실제 벡터 RAG 연결

변경 내용:

- 기본 embedding 차원을 `bge-m3` 기준 1024로 설정했다.
- SQLite 연결에서 `sqlite-vec` extension을 로드할 수 있게 했다.
- `chunk_embeddings` sqlite-vec 가상 테이블을 생성한다.
- 문서 chunk별 embedding을 `embeddings` 메타 테이블과 `chunk_embeddings` 벡터 테이블에 저장한다.
- 문서가 재분석되거나 삭제될 때 기존 embedding row도 함께 정리한다.
- RAG 질의응답은 `bge-m3`로 질문 embedding을 만든 뒤 sqlite-vec 벡터 검색을 먼저 사용한다.
- 벡터 검색을 사용할 수 없거나 결과가 없으면 기존 lexical 검색으로 fallback한다.
- RAG sources에 `search_mode`를 기록한다.
- Documents 페이지의 RAG 준비 상태에 embedding 차원과 저장된 벡터 row 수를 표시한다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- `sqlite-vec` 저장/검색 smoke 테스트 통과: 1024차원 더미 벡터 검색 거리 `0.0`
- `ollama list`에서 `qwen3:14b`, `qwen3:4b`, `bge-m3` 설치 확인
- `bge-m3` 실제 embedding 응답 확인: 1024차원, norm `1.0`
- 업로드 문서 기준 `semantic_search()` 실제 벡터 검색 확인
- RAG 작업 함수에서 sources `search_mode`가 `vector`로 기록되는지 확인

남은 작업:

- 실제 RAG 답변 품질과 검색 근거 순위를 관찰한다.
- `qwen3:4b` 기반 입출력 정제 AI를 연결한다.
- OCR 지원 범위와 우선순위를 정한다.

## 2026-06-06 v0.3.0 저장과 v0.3.1 개선 범위 분리

변경 내용:

- `v0.3.0`은 실제 embedding/RAG 연결 완료 상태로 저장한다.
- 예산안 RAG 질의응답 결과를 평가해 품질 개선 항목을 `v0.3.1`로 넘긴다.
- `v0.3.1` 개선 범위는 RAG 답변 품질, 표 형식 강제, 빈 응답 처리, chunk 우선순위 개선으로 둔다.

관찰한 문제:

- 질문 주제인 저출생, 보육, 청년 지원과 무관한 예산 항목이 답변에 섞였다.
- 표 요청을 Markdown 표로 지키지 못했다.
- 핵심 근거 chunk가 검색되었지만 1순위로 올라오지 않았다.
- 문서 요약에서 완료로 표시됐지만 내용이 비어 있는 사례가 있었다.

## 2026-06-06 v0.3.1 RAG 품질 개선

변경 내용:

- RAG 검색어에서 `저출생`, `보육`, `청년` 같은 핵심어만 추출하도록 했다.
- 벡터 검색 결과를 가져온 뒤 핵심어가 포함된 chunk에 가중치를 주어 재정렬한다.
- RAG 문서 근거에는 일치한 질문 키워드와 실제 파일명을 함께 넣는다.
- 표 요청이 있으면 Markdown 표 컬럼을 명시하고, 무관한 항목 제외 규칙을 강화했다.
- 근거 파일명은 허용된 파일명 그대로 쓰도록 제한했다.
- 금액은 같은 항목 근거 문장에 있는 수치만 쓰고, 확인되지 않으면 `문서에서 확인 안 됨`으로 쓰게 했다.
- LLM 응답이 비어 있으면 한 번 재시도하고, 그래도 비어 있으면 `LLM_EMPTY_RESPONSE`로 처리한다.
- 성공 결과 생성 시 body가 비어 있으면 성공 처리하지 않는다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- 예산안 질의 핵심어 추출 결과 확인: `저출생`, `보육`, `청년`
- 예산안 질의 상위 검색 결과가 관련 chunk 5, 2, 4 순서로 올라오는지 확인
- 빈 LLM 응답 재시도 smoke 테스트 통과
- 빈 성공 결과는 `LLM_EMPTY_RESPONSE` 예외로 차단되는지 확인
- 실제 RAG 호출에서 Markdown 표 형식과 실제 파일명 표시 확인

남은 작업:

- 실제 사용 중 금액과 chunk 번호 정확도를 추가 관찰한다.
- 필요하면 예산안처럼 숫자 추출이 중요한 질의에 별도 후처리 검증을 추가한다.

## 2026-06-06 v0.3.2 섹션형 RAG 질문 보정

변경 내용:

- `저출생·미래세대 지원`처럼 특정 섹션을 묻는 질문에서 작업 지시어가 검색 핵심어로 섞이는 문제를 줄였다.
- `사업`, `대상`, `증액`, `무관한`, `제외해줘` 같은 지시어를 검색 핵심어에서 제거했다.
- 섹션 제목이 포함된 chunk를 우선 선택하고, 바로 다음 chunk를 함께 컨텍스트로 사용한다.
- chunk 전체 대신 핵심어 주변 문맥만 LLM에 넘긴다.
- 증액 금액은 괄호 안 `+N` 금액만 사용하도록 프롬프트를 강화했다.
- 인원, 개소 수, 지원 비율, 대상 규모는 금액으로 쓰지 않도록 제한했다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- 예산안 섹션형 질문 핵심어 추출 결과 확인: `저출생`, `미래세대`, `보육`, `청년`
- 검색 결과 상위 chunk가 `4`, `5`, `2` 순서로 개선되는지 확인
- 최종 컨텍스트가 정답 섹션인 chunk `4`, `5`만 사용하는지 확인
- 실제 RAG 호출에서 지방거점성장, SOC, 취약계층 항목이 제거되는지 확인
- 실제 RAG 호출에서 증액 금액이 `+158억원`, `+18억원`, `+3억원`, `+445억원`, `+192억원`, `+54억원`처럼 정리되는지 확인

남은 작업:

- 숫자 추출 안정성을 더 높이려면 LLM 답변 후처리 검증을 검토한다.

## 2026-06-06 v0.3.3 구조화 청크와 Home 캐시 삭제

변경 내용:

- 문자 수 기반 청크를 fallback으로 유지하면서, PDF 텍스트에서는 섹션/항목 단위 chunk를 우선 생성한다.
- `[page N]`, `【 】`, `ㅇ`, `-` 패턴을 이용해 페이지, 섹션 제목, 항목을 감지한다.
- `chunks` 테이블에 `chunk_type`, `section_title`, `item_title`, `page_number`, `metadata_json` 컬럼을 추가했다.
- `analysis_version`을 추가해 파일이 바뀌지 않아도 v0.3.3 구조화 청크 기준으로 기존 문서를 재분석한다.
- RAG 검색에서 섹션 제목이 잡히면 해당 섹션의 item chunk 전체를 컨텍스트로 사용한다.
- candidate_id를 컨텍스트에 붙이고, 모델 응답에서 빠진 candidate는 누락 방지 후보로 보강한다.
- v0.3.2의 하드코딩 섹션 보정과 긴 excerpt 보정 코드를 줄였다.
- Home 결과 미리보기에 이전 결과와 Streamlit 캐시 삭제 버튼을 추가했다.

검증:

- `.venv\Scripts\python.exe -m compileall app.py src` 통과
- 예산안 PDF에서 `저출생 미래세대 지원` 섹션 item chunk 9개 생성 확인
- DB 재분석 후 `chunks` 구조화 metadata 저장 확인
- RAG 컨텍스트에 해당 섹션 item chunk 9개가 모두 들어가는지 확인
- candidate_id 누락 보강 smoke 테스트 통과
- 실제 RAG 호출에서 9개 후보가 모두 표에 표시되는지 확인

남은 작업:

- 문서별 형식이 달라질 때 섹션/항목 감지 패턴을 추가로 확장한다.
- 요약 작업의 숫자 단위 안정화는 별도 개선 후보로 유지한다.
