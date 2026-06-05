# 요구사항

## 프로젝트 정의

이 프로젝트는 로컬 환경에서 동작하는 작업 수행형 AI 비서다.

사용자가 자연어로 명령을 입력하면 프로그램이 의도를 분류하고, 파일 읽기, 문서 검색, 에러 분석, RAG 기반 질의응답 같은 작업을 실행한 뒤 결과를 Markdown과 SQLite에 저장한다.

## 기능 후보

아직 초기 구현 기능은 확정하지 않는다.

먼저 기본 실행 구조를 만들고, 아래 기능은 초기 후보로 둔다.

```txt
1. txt/md 파일 요약
2. 폴더 내 txt/md 문서 검색
3. 에러 메시지 분석
4. RAG 기반 문서 질의응답
```

## 먼저 확정할 기반 요구사항

- 사용자 명령을 정규화된 작업 JSON으로 변환한다.
- 작업 JSON은 코드에서 검증한다.
- 파일 입력, 모델 호출, 결과 저장, 오류 저장 흐름을 분리한다.
- 결과는 Markdown 파일로 저장한다.
- 실행 기록과 메타데이터는 SQLite에 저장한다.
- RAG가 필요한 경우 `bge-m3` 임베딩과 SQLite 기반 벡터 검색을 사용한다.
- 실패한 작업도 실행 기록과 오류 파일을 남긴다.

## 후보 사용자 시나리오

### 1. 문서 요약

입력:

```txt
uploads 폴더 안에 있는 txt 파일 요약해줘
```

완료 기준:

- 지정한 txt 파일을 읽는다.
- 핵심 내용을 요약한다.
- 결과를 화면에 출력한다.
- 실행 ID 기준 Markdown 파일로 저장한다.

### 2. 파일 검색

입력:

```txt
리눅스 자료 중 mount 관련 내용 찾아줘
```

완료 기준:

- 검색 키워드를 추출한다.
- 지정 폴더의 txt/md 파일을 검색한다.
- 관련 파일명과 문단을 출력한다.
- 결과를 실행 ID 기준 Markdown 파일로 저장한다.

### 3. 코드 오류 분석

입력:

```txt
Unresolved reference 'LocationServices'
Android Studio에서 이 에러가 떠
```

완료 기준:

- 에러 메시지를 분석한다.
- 에러 의미, 원인, 해결 방법, 확인할 파일, 수정 예시를 출력한다.
- 결과를 실행 ID 기준 Markdown 파일로 저장한다.

### 4. RAG 기반 문서 질의응답

입력:

```txt
uploads 폴더 자료를 기준으로 sqlite-vec 설치 방법 알려줘
```

완료 기준:

- 문서를 chunk로 나눈다.
- `bge-m3`로 embedding을 생성한다.
- SQLite 벡터 저장소에서 관련 chunk를 찾는다.
- 검색된 근거를 바탕으로 답변을 생성한다.
- 사용한 문서와 chunk 정보를 결과에 포함한다.

## 입출력 원칙

고정 파일명으로 덮어쓰지 않는다.

출력 파일은 실행 날짜, 작업 유형, 실행 ID를 포함한다.

```txt
outputs/
  2026-06-06/
    summarize_20260606_021530_a1b2c3.md
    rag_search_20260606_022010_d4e5f6.md
    rag_search_20260606_022010_d4e5f6.error.json
```

Markdown 결과에는 기본 메타데이터를 포함한다.

```md
---
task_type: rag_search
status: success
model: qwen3:14b
created_at: 2026-06-06 02:15:30
run_id: a1b2c3
---
```

## 실패 처리

사용자에게는 해결 가능한 안내를 보여주고, 내부에는 오류 코드를 저장한다.

초기 오류 코드는 아래를 사용한다.

```txt
EMPTY_COMMAND
UNKNOWN_COMMAND
MISSING_FILE
UNSUPPORTED_FILE_TYPE
FILE_TOO_LARGE
ENCODING_ERROR
OLLAMA_NOT_RUNNING
MODEL_NOT_FOUND
LLM_TIMEOUT
OUTPUT_WRITE_FAILED
DB_WRITE_FAILED
VECTOR_INDEX_FAILED
```

## 아직 확정하지 않는 기능

아래 기능은 나중에 확장한다.

- PDF 처리
- OCR
- 음성 인식
- TTS
- 일정 관리
- LoRA 학습
- Spring Boot API 서버
- React/FastAPI 기반 고도화

LoRA는 처음부터 적용하지 않는다. 먼저 입출력 정제 모델과 JSON schema로 데이터를 쌓고, 반복되는 입출력 패턴이 충분히 모이면 검토한다.

Spring Boot는 장기 백엔드 후보로 둔다. 로컬 단일 사용자 구조에서는 SQLite를 우선 사용하고, 다중 사용자, 권한 관리, 서버 API가 필요해질 때 Spring Boot와 PostgreSQL 확장을 검토한다.

## 기술 스택

| 구분 | 기술 |
| --- | --- |
| 언어 | Python |
| UI | Streamlit |
| 로컬 LLM 실행 | Ollama |
| 메인 응답 모델 | `qwen3:14b` |
| 입출력 정제 모델 | `qwen3:4b` |
| 임베딩 모델 | `bge-m3` |
| 파일 처리 | pathlib, os |
| 우선 문서 형식 | txt, md |
| 결과 저장 | Markdown |
| DB | SQLite |
| 현재 확인 SQLite 버전 | 3.49.1 |
| 벡터 검색 후보 | `sqlite-vec` |
