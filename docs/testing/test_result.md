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
- 파일 기반 상태 저장 유지 확인

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

## 2026-06-02 실행 문서 Command Prompt 기준 정리

테스트 범위:

- README 실행 명령어 표기 변경
- 테스트 계획 실행 명령어 표기 변경
- OpenAI API 키 설정 예시 변경

실행 결과:

- 실행 코드블록을 `cmd`로 변경
- API 키 설정 예시를 `set OPENAI_API_KEY=...`로 변경

비고:

- 문서 표기 변경이므로 앱 실행 테스트는 하지 않았다.

## 2026-06-02 좋은 예시 참고 개수 확대

테스트 범위:

- 좋은 예시 참고 개수를 10개로 변경
- 관련 문서 갱신

실행 결과:

- `node --check src\features\chat\chat.js` 통과

비고:

- 저장된 데이터 개수별 프롬프트 포함 여부는 앱에서 데이터 제작 후 수동 확인이 필요하다.

## 2026-06-02 좋은 예시 선택 기준 개선

테스트 범위:

- 좋은 예시 선택 로직을 최근순에서 점수 기반으로 변경
- 관련 문서 갱신

실행 결과:

- `node --check src\features\chat\chat.js` 통과

비고:

- 실제 프롬프트에 어떤 예시가 포함되는지는 저장 데이터가 있는 브라우저에서 수동 확인이 필요하다.

## 2026-06-02 제작 데이터 system 말투 충돌 수정

테스트 범위:

- 제작 탭 system prompt에 원하는 말투/형식 포함
- 초안 생성과 저장 시 같은 system prompt 사용
- 관련 문서 갱신

실행 결과:

- `node --check src\index.js` 통과

비고:

- 기존에 저장된 데이터는 자동으로 바뀌지 않으므로 다시 저장하거나 별도 마이그레이션이 필요하다.

## 2026-06-02 파일 기반 상태 저장 추가

테스트 범위:

- `/api/state` GET/PUT/DELETE 추가
- 브라우저 storage 모듈을 서버 API 기반으로 변경
- 앱 초기 로딩을 비동기 상태 로딩으로 변경

실행 결과:

- `node --check server.js` 통과
- `node --check src\index.js` 통과
- `node --check src\core\storage.js` 통과
- `GET /api/state`가 파일 없음 상태에서 `null` 응답
- `PUT /api/state`로 `data/app-state.json` 생성 확인
- `GET /api/state`로 저장 상태 재조회 확인
- `DELETE /api/state`로 테스트 상태 삭제 확인
