# src 구조 정리 계획

이 문서는 앞으로 `src` 코드를 어떻게 나눌지 정리한다. 현재는 기존 파일을 바로 옮기지 않고, 폴더 구조만 먼저 잡아둔다.

## 정리 방향

지금 `src/index.js`는 렌더링, 이벤트 연결, 상태 변경, 데이터 저장, 채팅, 데이터 제작 흐름을 많이 담당한다. MVP 단계에서는 빠르게 만들 수 있지만, 데이터 검수 기능과 학습 실험 기능이 추가되면 파일이 너무 커질 수 있다.

따라서 다음 원칙으로 천천히 분리한다.

- 기능이 추가될 때 관련 폴더로 새 코드를 둔다.
- 기존 코드는 한 번에 옮기지 않는다.
- 동작을 바꾸는 리팩터링은 작은 커밋으로 나눈다.
- `index` 역할의 파일은 필요할 때만 만든다.
- 파일보다 먼저 폴더의 책임을 명확히 한다.

## 목표 폴더 구조

```txt
src/
  core/
  features/
    profiles/
    memories/
    chat/
    dataset/
    data-maker/
    settings/
  ui/
  api/
  utils/
```

## 폴더별 역할

### `src/core`

앱 시작점, 전역 상태, 공통 흐름처럼 특정 기능 하나에 속하지 않는 코드를 둔다.

예상 대상:

- 앱 초기화
- 상태 초기값
- 상태 갱신 helper
- 화면 전체 렌더링 흐름

### `src/features/profiles`

AI 프로필 관련 기능을 둔다.

예상 대상:

- 프로필 생성
- 프로필 수정
- 프로필 요약
- 프로필별 메시지와 기억 연결

### `src/features/memories`

기억 관련 기능을 둔다.

예상 대상:

- 기억 추가
- 기억 삭제
- 질문과 관련 있는 기억 검색

### `src/features/chat`

채팅 관련 기능을 둔다.

예상 대상:

- 메시지 생성
- AI 답변 요청 흐름
- 좋은 답변 저장
- 답변 수정 저장
- 실패 기록

### `src/features/dataset`

학습 데이터 관리 기능을 둔다.

예상 대상:

- 학습 데이터 후보 생성
- 데이터 수정
- 데이터 삭제
- 검수 완료 처리
- 검수 완료 데이터 export
- JSONL 변환

### `src/features/data-maker`

데이터 제작 탭의 흐름을 둔다.

예상 대상:

- 질문, 핵심 사실, 말투 조건 입력 처리
- AI 초안 생성 요청
- 최종 답변 저장

### `src/features/settings`

앱 설정 관련 기능을 둔다.

예상 대상:

- AI 제공자 선택
- Ollama 모델 설정
- OpenAI 모델 설정
- 기본 설정값 관리

### `src/ui`

화면 렌더링과 DOM 조립 코드를 둔다.

예상 대상:

- 탭 전환
- 채팅 목록 렌더링
- 데이터 목록 렌더링
- 프로필 목록 렌더링
- 빈 상태 UI

### `src/api`

브라우저에서 서버 API를 호출하는 코드를 둔다.

예상 대상:

- `/api/chat` 호출
- API 오류 메시지 정리

### `src/utils`

여러 기능에서 공유하는 작은 도구를 둔다.

예상 대상:

- 중국어 한자 감지
- 날짜 포맷
- 문자열 정리
- 입력값 검증

## 현재 파일 배치

| 파일 | 역할 |
| --- | --- |
| `src/index.js` | 앱 진입점, 전체 렌더링과 이벤트 연결 |
| `src/core/promptBuilder.js` | 시스템 프롬프트 생성 |
| `src/core/storage.js` | `/api/state` 저장 요청과 파일 다운로드 |
| `src/features/profiles/profiles.js` | AI 프로필 생성, 수정, 요약 |
| `src/features/memories/memories.js` | 기억 추가, 삭제, 관련 기억 검색 |
| `src/features/chat/chat.js` | 채팅 메시지 생성과 AI 답변 요청 흐름 |
| `src/features/dataset/dataset.js` | 학습 데이터 후보 생성과 JSONL 변환 |

## 아직 더 분리할 후보

| 현재 위치 | 나중에 둘 위치 |
| --- | --- |
| `src/index.js`의 데이터 목록 렌더링 | `src/ui/` |
| `src/index.js`의 데이터 제작 탭 흐름 | `src/features/data-maker/` |
| `src/index.js`의 설정 처리 | `src/features/settings/` |
| `src/features/chat/chat.js`의 `/api/chat` 호출 | `src/api/` |

## 첫 리팩터링 후보

다음 기능을 만들기 전에 `dataset` 영역부터 분리하는 것이 좋다.

1. 데이터 목록 렌더링 분리
2. JSONL export 로직 분리
3. 데이터 검수 상태 추가
4. 검수 완료 데이터만 export

## 주의할 점

- 폴더를 만들었다고 바로 파일을 억지로 옮기지 않는다.
- import 경로 변경은 동작이 깨지기 쉬우므로 작은 단위로 확인한다.
- 기능 구현과 대규모 파일 이동을 같은 커밋에 섞지 않는다.
