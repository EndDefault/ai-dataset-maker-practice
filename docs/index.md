# 문서 목록

이 프로젝트는 docs-first 방식으로 진행한다. 구현 전에 목표, 범위, 데이터 구조, 학습 흐름, 평가 기준을 문서로 먼저 고정한다.

## 핵심 문서

| 문서 | 용도 |
| --- | --- |
| `project-status.md` | 현재 상태와 다음 작업 요약 |
| `planning/vision.md` | 프로젝트 정의와 최종 목표 |
| `planning/requirements.md` | 사용자 시나리오와 요구사항 |
| `planning/roadmap.md` | MVP부터 확장까지 개발 순서 |
| `planning/checklist.md` | 단계별 체크리스트 |
| `planning/decision_log.md` | 중요한 결정과 이유 |
| `design/architecture.md` | 전체 시스템 구조 |
| `design/data_model.md` | JSON 후보, 상태값, JSONL 구조 |
| `design/ui_flow.md` | 화면 흐름 |
| `design/training_pipeline.md` | PyTorch/PEFT 학습 흐름 |
| `design/rag_design.md` | RAG 참고 자료 설계 |
| `development/setup.md` | 설치와 실행 방법 |
| `development/command_guide.md` | Windows cmd 기준 명령어 |
| `development/commit_convention.md` | 커밋 규칙 |
| `development/dataset_rules.md` | 데이터 제작과 검수 규칙 |
| `testing/test_plan.md` | 테스트 전략 |
| `testing/test_result.md` | 테스트 결과 기록 |
| `testing/evaluation_criteria.md` | 데이터와 모델 평가 기준 |
| `logs/implementation_log.md` | 구현 기록 |
| `logs/experiment_log.md` | 학습 실험 기록 |
| `logs/bugfix_log.md` | 버그 수정 기록 |
| `reference/glossary.md` | 용어 정리 |
| `reference/ai_learning_notes.md` | AI 학습 개념 노트 |

## 갱신 규칙

- 기능을 만들기 전에는 관련 `planning` 또는 `design` 문서를 먼저 확인한다.
- 기능을 만든 뒤에는 `project-status.md`, `planning/checklist.md`, `logs/implementation_log.md`를 갱신한다.
- 데이터 구조를 바꾸면 `design/data_model.md`와 `testing/test_plan.md`를 갱신한다.
- 학습 실험을 하면 `logs/experiment_log.md`와 `testing/evaluation_criteria.md`를 갱신한다.
- 버그를 고치면 `logs/bugfix_log.md`에 재현 조건과 수정 내용을 남긴다.
- 명령어 문서는 Windows `cmd` 기준으로 작성한다.
