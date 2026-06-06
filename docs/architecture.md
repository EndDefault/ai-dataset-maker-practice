# 아키텍처

## 전체 흐름

```txt
[사용자 명령 입력]
        ↓
[입출력 정제 AI]
        ↓
[작업 JSON 생성]
        ↓
[JSON schema 검증]
        ↓
[작업 실행]
 ├─ 문서 요약
 ├─ 파일 검색
 ├─ 코드 오류 분석
 └─ RAG 문서 질의응답
        ↓
[메인 AI 응답 생성]
        ↓
[출력 검증]
        ↓
[결과 출력]
        ↓
[Markdown, SQLite, 오류 파일 저장]
```

## 모듈 구조 초안

```txt
app.py
src/
  config.py
  schemas.py
  command_router.py
  ui/
    app/
      home/
        page.py
      documents/
        page.py
      runs/
        page.py
      settings/
        page.py
    features/
      home/
        command_input.py
        result_preview.py
        run_status.py
      documents/
        upload_panel.py
        document_table.py
        chunk_preview.py
        embedding_status.py
      runs/
        run_history.py
        artifact_viewer.py
        error_detail.py
      settings/
        model_settings.py
        database_settings.py
        path_settings.py
    shared/
      layout.py
      navigation.py
      state.py
      components.py
      messages.py
  llm/
    ollama_client.py
  normalization/
    io_cleaner.py
  tasks/
    summarize.py
    search.py
    explain_error.py
    rag_search.py
  rag/
    chunker.py
    embedding_client.py
    vector_store.py
  storage/
    sqlite_store.py
    markdown_writer.py
    error_writer.py
data/
  app.db
uploads/
outputs/
docs/
```

## 모듈 역할

| 모듈 | 역할 |
| --- | --- |
| `app.py` | Streamlit UI 진입점 |
| `config.py` | 모델명, 경로, timeout 설정 |
| `schemas.py` | 작업 JSON과 결과 schema 정의 |
| `command_router.py` | 정제된 작업 JSON을 실제 작업 함수로 연결 |
| `ui/app/*/page.py` | 페이지 조립 |
| `ui/features/*` | 페이지별 UI 기능과 화면 로직 |
| `ui/shared/*` | 공통 레이아웃, 네비게이션, 상태, 컴포넌트 |
| `ollama_client.py` | Ollama 로컬 LLM 호출 |
| `io_cleaner.py` | 사용자 입력을 정규화된 작업 JSON으로 변환 |
| `summarize.py` | txt/md/pdf 파일 요약 |
| `search.py` | txt/md/pdf 파일 키워드 검색 |
| `explain_error.py` | 에러 메시지 분석 |
| `rag_search.py` | RAG 기반 질의응답 |
| `chunker.py` | 문서를 검색 가능한 chunk로 분리 |
| `embedding_client.py` | `bge-m3` embedding 생성 |
| `vector_store.py` | SQLite 벡터 검색 처리 |
| `sqlite_store.py` | 실행 기록, 문서, chunk, 결과, 오류 저장 |
| `markdown_writer.py` | 결과를 Markdown 파일로 저장 |
| `error_writer.py` | 오류 상세 정보를 JSON 파일로 저장 |

## 모델 역할

| 역할 | 모델 | 용도 |
| --- | --- | --- |
| 메인 AI | `qwen3:14b` | 최종 답변, 요약, 에러 분석 설명 생성 |
| 입출력 정제 AI | `qwen3:4b` | 명령 정규화, 작업 JSON 생성, 출력 검증 |
| 임베딩 모델 | `bge-m3` | 문서 chunk와 질문 embedding 생성 |

기준 장비는 RTX 5060 Ti 16GB다.

## UI 구조

UI는 Streamlit으로 시작한다.

단, 파일 구조는 Next.js의 `app/페이지명/page` 패턴을 참고해서 페이지와 기능을 분리한다.

```txt
src/ui/
  app/
    home/
      page.py
    documents/
      page.py
    runs/
      page.py
    settings/
      page.py
  features/
    home/
      command_input.py
      result_preview.py
      run_status.py
    documents/
      upload_panel.py
      document_table.py
      chunk_preview.py
      embedding_status.py
    runs/
      run_history.py
      artifact_viewer.py
      error_detail.py
    settings/
      model_settings.py
      database_settings.py
      path_settings.py
  shared/
    layout.py
    navigation.py
    state.py
    components.py
    messages.py
```

### UI 역할 분리

| 위치 | 역할 |
| --- | --- |
| `ui/app/home/page.py` | 명령 입력, 실행 상태, 결과 미리보기 화면 조립 |
| `ui/app/documents/page.py` | 문서 업로드, chunk, embedding 상태 화면 조립 |
| `ui/app/runs/page.py` | 실행 기록, 산출물, 오류 상세 화면 조립 |
| `ui/app/settings/page.py` | 모델, DB, 경로, timeout 설정 화면 조립 |
| `ui/features/<page>/` | 해당 페이지에서만 쓰는 UI 조각과 이벤트 처리 |
| `ui/shared/` | 여러 페이지에서 재사용하는 공통 UI |

`page.py`는 화면 조립만 담당한다. 실제 입력 처리, 테이블 표시, 상태 메시지, 결과 미리보기 같은 세부 UI는 `features/페이지명/` 아래에 둔다.

예시:

```python
from src.ui.features.home.command_input import render_command_input
from src.ui.features.home.result_preview import render_result_preview
from src.ui.features.home.run_status import render_run_status


def render():
    command = render_command_input()
    render_run_status()
    render_result_preview()
```

## UI/UX 방향

초기 UI는 챗봇보다 작업 콘솔에 가깝게 만든다.

주요 화면은 아래처럼 나눈다.

| 페이지 | 목적 |
| --- | --- |
| Home | 자연어 명령 입력, 작업 실행, Markdown 결과 미리보기 |
| Documents | 파일 업로드, 문서 목록, chunk/embedding 상태 확인 |
| Runs | 과거 실행 기록, 출력 Markdown, `error.json` 확인 |
| Settings | Ollama 모델, SQLite 경로, timeout, 출력 경로 설정 |

화면 구성 원칙:

- 상단 또는 중앙에 자연어 명령 입력창을 둔다.
- Home에서는 업로드된 문서를 하나씩 추가해 이번 작업 입력 파일 목록을 만든다.
- 선택한 입력 파일은 실행 전 삭제할 수 있고, 추가 버튼은 계속 사용할 수 있게 둔다.
- 사이드바에는 현재 모델과 페이지 네비게이션을 둔다.
- 결과는 Markdown 미리보기 중심으로 보여준다.
- 실행 기록과 오류는 숨기지 않고 바로 추적 가능하게 둔다.
- RAG 답변에는 사용한 문서와 chunk 정보를 함께 보여준다.
- UI는 화려한 챗봇보다 조용하고 밀도 있는 로컬 작업 도구를 목표로 한다.

## 작업 JSON 초안

입출력 정제 AI는 자유 문장을 바로 실행하지 않고 아래 형태의 JSON을 만든다.

```json
{
  "task_type": "rag_search",
  "query": "mount 관련 내용",
  "input_paths": ["uploads"],
  "output_format": "markdown",
  "include_error_file": true
}
```

## 명령 분류 방식

초기에는 입출력 정제 AI가 작업 JSON을 만들고, 코드가 schema를 검증한다.

정제 AI가 실패하거나 JSON이 유효하지 않으면 단순 키워드 규칙을 fallback으로 사용한다.

```python
if "요약" in command:
    task = "summarize"
elif "찾아" in command or "검색" in command:
    task = "search"
elif "에러" in command or "오류" in command:
    task = "explain_error"
```

## RAG 흐름

```txt
[문서 수집]
        ↓
[페이지/섹션/항목 기반 chunk 분리]
        ↓
[`bge-m3` embedding 생성]
        ↓
[SQLite + sqlite-vec 저장]
        ↓
[사용자 질문 embedding]
        ↓
[sqlite-vec 관련 chunk 검색]
        ↓
[`qwen3:14b` 답변 생성]
```

`sqlite-vec`는 Python 가상환경에 설치해서 사용한다. RAG 질의응답은 벡터 검색을 먼저 사용하고, sqlite-vec 또는 embedding 호출을 사용할 수 없으면 lexical fallback 검색으로 대체한다.

## SQLite 테이블 초안

| 테이블 | 용도 |
| --- | --- |
| `runs` | 작업 실행 기록 |
| `documents` | 입력 문서 메타데이터, 처리 상태, PDF 페이지 수, 추출 글자 수, chunk 수 |
| `chunks` | 검색 단위 chunk와 `chunk_type`, `section_title`, `item_title`, `page_number`, `metadata_json` |
| `embeddings` | chunk embedding 메타데이터와 JSON 백업 |
| `chunk_embeddings` | `sqlite-vec` 가상 테이블, 실제 벡터 검색 대상 |
| `artifacts` | Markdown, error.json 같은 산출물 경로 |
| `errors` | 오류 코드와 상세 메시지 |

## 결과 저장 원칙

- 모든 작업 결과는 화면에 먼저 보여준다.
- 사용자가 재사용할 수 있게 Markdown 파일로 저장한다.
- 기본 저장 위치는 `outputs/`로 한다.
- 파일 이름은 작업 유형, 시간, 실행 ID 기준으로 만든다.
- 실패한 작업은 Markdown 요약과 별도 `error.json`을 함께 저장한다.
