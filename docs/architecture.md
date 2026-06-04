# 아키텍처

## 전체 흐름

```txt
[사용자 명령 입력]
        ↓
[명령 유형 분류]
        ↓
[작업 실행]
 ├─ 문서 요약
 ├─ 파일 검색
 └─ 코드 오류 분석
        ↓
[로컬 LLM 응답 생성]
        ↓
[결과 출력]
        ↓
[Markdown 파일 저장]
```

## 모듈 구조 초안

```txt
app.py
src/
  command_router.py
  llm_client.py
  tasks/
    summarize.py
    search.py
    explain_error.py
  storage/
    markdown_writer.py
uploads/
outputs/
docs/
```

## 모듈 역할

| 모듈 | 역할 |
| --- | --- |
| `app.py` | Streamlit UI 진입점 |
| `command_router.py` | 자연어 명령을 작업 유형으로 분류 |
| `llm_client.py` | Ollama 로컬 LLM 호출 |
| `summarize.py` | txt 파일 요약 |
| `search.py` | txt/md 파일 키워드 검색 |
| `explain_error.py` | 에러 메시지 분석 |
| `markdown_writer.py` | 결과를 Markdown 파일로 저장 |

## 명령 분류 방식

초기에는 단순 키워드 규칙으로 시작한다.

```python
if "요약" in command:
    task = "summarize"
elif "찾아" in command or "검색" in command:
    task = "search"
elif "에러" in command or "오류" in command:
    task = "explain_error"
```

나중에 필요하면 로컬 LLM을 이용한 명령 분류로 확장한다.

## 결과 저장 원칙

- 모든 작업 결과는 화면에 먼저 보여준다.
- 사용자가 재사용할 수 있게 Markdown 파일로 저장한다.
- 기본 저장 위치는 `outputs/`로 한다.
- 파일 이름은 작업 유형과 시간 기준으로 만든다.
