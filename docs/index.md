# AI Maker Studio 문서 목록

프로젝트 문서는 목적별로 나누어 관리한다. 구현이 바뀌면 관련 문서를 같이 갱신한다.

## 핵심 문서

| 문서 | 용도 |
| --- | --- |
| `project-status.md` | 현재 진행 상태와 다음 작업 |
| `portfolio-direction.md` | 포트폴리오 관점의 문제 정의, 구조, 한계, 개선 방향 |
| `requirements.md` | 사용자 시나리오, 기능 요구사항, 비기능 요구사항 |
| `data.md` | 데이터 모델, 저장 구조, JSONL export 형식 |
| `checklist.md` | 단계별 개발 체크리스트 |
| `test_plan.md` | 테스트 전략, 테스트 케이스, 실행 방법 |
| `test_result.md` | 테스트 실행 결과 기록 |
| `implementation_log.md` | 구현 이력, 설계 결정, 트레이드오프 |
| `bugfix_log.md` | 버그 재현 조건, 원인, 수정 내역, 회귀 방지 |
| `ui_index.md` | 주요 화면과 UI 구성 |
| `seed_data.md` | 초기 데이터와 테스트 데이터 설계 |
| `commit_convention.md` | 커밋 메시지 규칙과 기능 단위 커밋 기준 |

## 문서 갱신 규칙

- 기능을 추가하면 `requirements.md`, `checklist.md`, `implementation_log.md`를 확인한다.
- 데이터 구조가 바뀌면 `data.md`, `test_plan.md`, `test_result.md`를 확인한다.
- 버그를 고치면 `bugfix_log.md`에 재현 조건과 수정 내용을 남긴다.
- 포트폴리오에 설명할 수 있는 결정이 생기면 `portfolio-direction.md`에 기록한다.
- 커밋 전에는 `commit_convention.md`의 제목 형식과 커밋 단위를 확인한다.
