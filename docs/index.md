# 문서 목록

이 프로젝트는 로컬 LLM과 RAG 구조를 연습하기 위한 docs-first 프로젝트다.

목표는 완성형 서비스가 아니라, **AI를 활용해 로컬 RAG 앱을 만들고, 실행 결과를 확인하고, 한계를 문서로 남기는 것**이다.

## 현재 정리

- 1차 구현은 종료 상태로 둔다.
- 현재 앱은 Streamlit 기반 로컬 작업 콘솔이다.
- RAG는 `bge-m3` embedding, SQLite, `sqlite-vec`, `qwen3:14b`를 사용한다.
- 평가 스크립트는 `evals/rag/`에 둔다.
- `qwen3:4b` 기반 입력 정제 AI는 아직 실제 연결 전이다.
- OCR, 깊은 평가, 정교한 UI/UX는 다음 단계 후보로 남긴다.

## 핵심 문서

| 문서 | 용도 |
| --- | --- |
| `project-status.md` | 1차 종료 기준, 현재 상태, 다음 후보 작업 |
| `ai-collaboration.md` | AI를 어떻게 활용했는지와 배운 점 |
| `requirements.md` | 초기 요구사항, 기능 후보, 결정 대기 항목 |
| `architecture.md` | 전체 구조, 모델 역할, RAG/DB 흐름 |
| `checklist.md` | 단계별 작업 체크리스트 |
| `command_guide.md` | Windows cmd 기준 실행 명령어 |
| `commit_convention.md` | 커밋 규칙 |
| `implementation_log.md` | 구현 기록 |
| `version_plan.md` | 버전 계획과 실험 기록 |
| `../evals/rag/README.md` | RAG 평가 스크립트 설명 |

## 현재 프로젝트를 읽는 순서

1. `README.md`
2. `docs/project-status.md`
3. `docs/ai-collaboration.md`
4. `docs/architecture.md`
5. `evals/rag/README.md`

코드보다 프로젝트 의도를 먼저 보려면 위 순서가 가장 낫다.

## 갱신 규칙

- 기능을 만들기 전에는 `requirements.md`, `architecture.md`, `checklist.md`를 먼저 확인한다.
- 구조가 바뀌면 `architecture.md`를 갱신한다.
- 구현이 끝나면 `project-status.md`, `checklist.md`, `implementation_log.md`를 갱신한다.
- 실행 명령이 바뀌면 `command_guide.md`를 갱신한다.
- 평가 방식이 바뀌면 `evals/rag/README.md`와 `docs/project-status.md`를 함께 갱신한다.
- 모든 명령어 예시는 Windows `cmd` 기준으로 작성한다.
- PowerShell 전용 명령어를 기본 문서에 쓰지 않는다.

## 다음에 문서화할 후보

아래 항목이 실제 작업으로 커질 때만 새 문서를 만든다.

```txt
PDF 파싱 품질 점검 → docs/pdf.md
OCR 도입 검토 → docs/ocr.md
RAG 평가 기준 강화 → docs/rag-evaluation.md
UI 규칙 재설계 → docs/ui-guidelines.md
Codex Skill 도입 → docs/codex-skill-notes.md
```
