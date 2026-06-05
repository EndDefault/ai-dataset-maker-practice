# 문서 목록

이 프로젝트는 docs-first 방식으로 진행한다. 지금은 기능을 확정하기보다 로컬 작업 비서의 기본 실행 구조를 먼저 정한다.

목표는 단순 챗봇이 아니라, 실제 파일을 읽고 결과를 Markdown으로 저장하는 **로컬 작업 수행형 AI 비서**를 만드는 것이다.

## 현재 결정

- 초기 구현 기능은 아직 확정하지 않는다.
- 초기 후보 기능은 txt/md/pdf 요약, 문서 검색, 에러 분석, RAG 질의응답이다.
- RTX 5060 Ti 16GB 기준으로 `qwen3:14b`, `qwen3:4b`, `bge-m3`를 우선 사용한다.
- DB는 SQLite를 기본으로 하고, 벡터 검색은 `sqlite-vec`를 우선 검토한다.
- Python 패키지는 프로젝트 가상환경 `.venv`에 설치한다.

## 핵심 문서

| 문서 | 용도 |
| --- | --- |
| `project-status.md` | 현재 상태와 다음 작업 요약 |
| `requirements.md` | 요구사항, 기능 후보, 결정 대기 항목 |
| `architecture.md` | 전체 구조, 모델 역할, RAG/DB 흐름 |
| `checklist.md` | 단계별 작업 체크리스트 |
| `command_guide.md` | Windows cmd 기준 실행 명령어 |
| `commit_convention.md` | 계속 사용할 커밋 규칙 |
| `implementation_log.md` | 구현 기록 |

## 갱신 규칙

- 기능을 만들기 전에는 `requirements.md`, `architecture.md`, `checklist.md`를 먼저 확인한다.
- 구조가 바뀌면 `architecture.md`를 갱신한다.
- 구현이 끝나면 `project-status.md`, `checklist.md`, `implementation_log.md`를 갱신한다.
- 실행 명령이 바뀌면 `command_guide.md`를 갱신한다.
- 모든 명령어 예시는 Windows `cmd` 기준으로 작성한다.
- PowerShell 전용 명령어를 기본 문서에 쓰지 않는다.

## 확장 문서 규칙

처음부터 문서를 많이 만들지 않는다.

기능이 커질 때만 새 문서를 추가한다.

예시:

```txt
PDF 기능이 커지면 docs/pdf.md 추가
OCR 기능이 커지면 docs/ocr.md 추가
RAG 기능이 커지면 docs/rag.md 추가
음성 기능이 커지면 docs/voice.md 추가
```
