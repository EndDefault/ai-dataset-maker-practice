# AI Maker Studio 문서 목록

프로젝트 문서는 목적별로 나누어 관리한다. 구현이 바뀌면 관련 문서를 같이 갱신한다.

## 핵심 문서

| 문서 | 용도 |
| --- | --- |
| `project-status.md` | 현재 진행 상태와 다음 작업 |
| `planning/portfolio-direction.md` | 포트폴리오 관점의 문제 정의, 구조, 한계, 개선 방향 |
| `planning/requirements.md` | 사용자 시나리오, 기능 요구사항, 비기능 요구사항 |
| `planning/checklist.md` | 단계별 개발 체크리스트 |
| `planning/decision_log.md` | 중요한 의사결정과 이유 |
| `planning/refactor_plan.md` | 리팩터링 순서와 기준 |
| `design/architecture.md` | 전체 아키텍처와 데이터 흐름 |
| `design/data.md` | 데이터 모델, 저장 구조, JSONL export 형식 |
| `design/ui_index.md` | 주요 화면과 UI 구성 |
| `design/src_structure.md` | `src` 폴더 구조 정리 계획 |
| `development/commit_convention.md` | 커밋 메시지 규칙과 기능 단위 커밋 기준 |
| `development/seed_data.md` | 초기 데이터와 테스트 데이터 설계 |
| `development/curated_dataset.md` | 직접 검수한 50개 기준 데이터셋 생성 방식 |
| `testing/test_plan.md` | 테스트 전략, 테스트 케이스, 실행 방법 |
| `testing/test_result.md` | 테스트 실행 결과 기록 |
| `logs/implementation_log.md` | 구현 이력, 설계 결정, 트레이드오프 |
| `logs/bugfix_log.md` | 버그 재현 조건, 원인, 수정 내역, 회귀 방지 |
| `reference/glossary.md` | 용어와 핵심 로직 공부 노트 |

## 폴더 구조

```txt
docs/
  planning/      기획, 요구사항, 방향성, 리팩터링 계획
  design/        아키텍처, 데이터 모델, UI, src 구조
  development/   개발 규칙과 테스트 데이터
  testing/       테스트 계획과 결과
  logs/          구현 이력과 버그 수정 기록
  reference/     공부용 용어와 핵심 로직 정리
```

## 문서 갱신 규칙

- 기능을 추가하면 `planning/requirements.md`, `planning/checklist.md`, `logs/implementation_log.md`를 확인한다.
- 데이터 구조가 바뀌면 `design/data.md`, `testing/test_plan.md`, `testing/test_result.md`를 확인한다.
- 버그를 고치면 `logs/bugfix_log.md`에 재현 조건과 수정 내용을 남긴다.
- 포트폴리오에 설명할 수 있는 결정이 생기면 `planning/portfolio-direction.md`와 `planning/decision_log.md`에 기록한다.
- 커밋 전에는 `development/commit_convention.md`의 제목 형식과 커밋 단위를 확인한다.
- 코드 구조를 바꾸기 전에는 `design/src_structure.md`와 `planning/refactor_plan.md`를 확인한다.
- 새 개념이나 핵심 로직을 배우면 `reference/glossary.md`에 내 말로 정리한다.
