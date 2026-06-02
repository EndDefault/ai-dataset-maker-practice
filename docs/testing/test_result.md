# 테스트 결과

테스트를 실행할 때마다 이 문서에 날짜, 범위, 결과, 발견한 문제를 기록한다.

## 2026-06-02 문서 분리 작업

테스트 범위:

- 문서 생성과 문서 링크 정리
- 기존 상태 문서와 새 문서의 역할 분리

실행 결과:

- `docs/index.md` 추가
- `docs/planning/requirements.md` 추가
- `docs/design/data.md` 추가
- `docs/development/seed_data.md` 추가
- `docs/planning/checklist.md` 추가
- `docs/testing/test_plan.md` 추가
- `docs/testing/test_result.md` 추가
- `docs/logs/implementation_log.md` 추가
- `docs/logs/bugfix_log.md` 추가
- `docs/design/ui_index.md` 추가

비고:

- 이번 작업은 문서 구조 정리이므로 앱 실행 테스트는 하지 않았다.

## 다음 테스트 예정

- 데이터셋 검수 기능 구현 후 수동 테스트
- JSONL export 포맷 확인
- 브라우저 localStorage 유지 확인

## 2026-06-02 커밋 규칙 문서 추가

테스트 범위:

- 커밋 규칙 문서 추가
- 문서 목록과 상태 문서에 링크 반영

실행 결과:

- `docs/development/commit_convention.md` 추가
- `docs/index.md` 갱신
- `docs/project-status.md` 갱신
- `docs/logs/implementation_log.md` 갱신

비고:

- 문서 변경이므로 앱 실행 테스트는 하지 않았다.

## 2026-06-02 src 폴더 구조 계획 추가

테스트 범위:

- 폴더 구조 추가
- `docs/design/src_structure.md` 추가
- 문서 목록과 구현 로그 갱신

실행 결과:

- `src/core`, `src/features`, `src/ui`, `src/api`, `src/utils` 폴더 추가
- 기능별 하위 폴더 추가
- 기존 JavaScript 파일은 이동하지 않음

비고:

- 실행 경로를 바꾸지 않았으므로 앱 실행 테스트는 하지 않았다.

## 2026-06-02 docs 폴더 구조 분리

테스트 범위:

- 기존 문서의 목적별 폴더 이동
- 새 기획, 설계, 참고 문서 추가
- 문서 목록과 상태 문서의 경로 갱신

실행 결과:

- `docs/planning`, `docs/design`, `docs/development`, `docs/testing`, `docs/logs`, `docs/reference` 폴더 추가
- `docs/planning/decision_log.md`, `docs/planning/refactor_plan.md`, `docs/design/architecture.md`, `docs/reference/glossary.md` 추가
- `docs/index.md`와 `docs/project-status.md`의 문서 경로 갱신

비고:

- 문서 구조 변경이므로 앱 실행 테스트는 하지 않았다.

## 2026-06-02 기존 JavaScript 파일 구조 재배치

테스트 범위:

- 기존 JavaScript 파일을 새 `src` 구조로 이동
- import 경로 수정
- HTML 모듈 진입점 수정

실행 결과:

- `src/index.js`를 앱 진입점으로 변경
- `src/core`와 `src/features` 하위로 기존 모듈 이동
- 앱 실행 테스트 예정
