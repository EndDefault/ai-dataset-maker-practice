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

## 2026-06-02 API 클라이언트 모듈 분리

테스트 범위:

- `/api/chat` 호출 모듈 분리
- `/api/state` 호출 모듈 분리
- 기존 호출부 import 경로 수정

실행 결과:

- `node --check src\api\chatApi.js` 통과
- `node --check src\api\stateApi.js` 통과
- `node --check src\features\chat\chat.js` 통과
- `node --check src\index.js` 통과
- `src` 내 `fetch` 호출이 `src/api` 폴더에만 남아 있는지 확인

## 2026-06-02 더미 상태 생성 스크립트 추가

테스트 범위:

- seed 문서 기반 더미 상태 생성
- 생성된 상태 파일의 프로필과 dataset 개수 확인
- `data/app-state.json` Git ignore 확인

실행 결과:

- `node --check scripts\create-seed-state.js` 통과
- `node scripts\create-seed-state.js` 실행 성공
- `data/app-state.json` 생성 확인
- 프로필 1개, dataset 15개 확인
- 첫 번째 dataset의 system 메시지에 `원하는 말투와 형식` 포함 확인
- `git check-ignore -v data\app-state.json`으로 Git 제외 확인

## 2026-06-02 냥체 프롬프트 오염 방지

테스트 범위:

- AI 요청의 최근 대화 메시지 필터 변경
- 시스템 프롬프트 냥체 규칙 강화
- 말투 선택 옵션 추가

실행 결과:

- `node --check src\features\chat\chat.js` 통과
- `node --check src\core\promptBuilder.js` 통과
- `node --check src\index.js` 통과
- `node --check scripts\create-seed-state.js` 통과

비고:

- 현재 `data/app-state.json`의 실패 대화 기록은 비우고, `나비` 프로필 말투를 `자연스러운 냥체`로 맞췄다.

## 2026-06-02 저장 데이터 수정/삭제 추가

테스트 범위:

- 좋은 예시 목록에 수정/삭제 버튼 추가
- 수정 시 dataset의 assistant 메시지 갱신
- 삭제 시 dataset에서 항목 제거

실행 결과:

- `node --check src\index.js` 통과

## 2026-06-02 좋은 예시 오염 방지 프롬프트 조정

테스트 범위:

- 좋은 예시 포함 개수 축소
- 시스템 프롬프트의 예시 복사 금지 규칙 추가

실행 결과:

- `node --check src\core\promptBuilder.js` 통과
- `node --check src\features\chat\chat.js` 통과

## 2026-06-02 큐레이션 데이터 50개 생성

테스트 범위:

- 큐레이션 데이터 생성 스크립트 문법 확인
- 생성 예시 개수 50개 확인
- `data/app-state.json` 생성 결과 확인
- assistant 답변의 냥체 끝맺음 확인
- 프로필 대화 기록 초기화 확인

실행 결과:

- `node --check scripts\create-curated-state.js` 통과
- `rg -c "question:" scripts\create-curated-state.js` 결과 50
- `node scripts\create-curated-state.js` 실행 성공
- 생성된 dataset 50개 확인
- 생성된 dataset source가 모두 `curated`임을 확인
- profile messages 0개 확인
- assistant 답변 끝맺음 검사에서 문제 0개 확인
