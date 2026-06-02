# 아키텍처 개요

이 문서는 AI Maker Studio의 전체 구조와 데이터 흐름을 설명한다.

## 전체 구조

```txt
Browser UI
→ src JavaScript
→ localStorage
→ JSONL export

Browser UI
→ /api/chat
→ practice / Ollama / OpenAI
→ AI response
→ Browser UI
```

## 주요 구성 요소

### Browser UI

사용자가 실제로 조작하는 화면이다.

역할:

- AI 프로필 설정
- 기억 추가와 삭제
- 채팅 실험
- 데이터 제작
- 데이터셋 확인
- JSONL export

### Frontend JavaScript

브라우저에서 동작하는 앱 로직이다.

현재 주요 파일:

- `src/app.js`: 화면 렌더링과 이벤트 연결
- `src/chat.js`: AI 답변 요청 흐름
- `src/dataset.js`: 학습 데이터 후보 생성과 JSONL 변환
- `src/profiles.js`: AI 프로필 생성과 수정
- `src/memories.js`: 기억 추가, 삭제, 관련 기억 검색
- `src/promptBuilder.js`: 시스템 프롬프트 생성
- `src/storage.js`: localStorage 저장과 파일 다운로드

앞으로는 `src/features`, `src/ui`, `src/api`, `src/core`, `src/utils`로 점진 분리한다.

### Server

`server.js`는 정적 파일을 제공하고 `/api/chat` 요청을 처리한다.

역할:

- 앱 파일 제공
- AI 제공자 선택
- Ollama API 호출
- OpenAI API 호출
- practice 응답 생성

### AI Providers

현재 제공자는 세 가지다.

- `practice`: 비용 없이 흐름을 테스트하는 가짜 응답
- `ollama`: 로컬 Ollama 모델 호출
- `openai`: OpenAI API 호출

### Storage

현재 저장소는 브라우저 `localStorage`다.

저장 대상:

- AI 프로필
- 기억
- 채팅 메시지
- 학습 데이터 후보
- 실패 기록
- 앱 설정

## 데이터 제작 흐름

```txt
사용자 입력
→ 질문, 핵심 사실, 말투 조건 작성
→ 시스템 프롬프트 생성
→ AI 초안 생성
→ 사람이 최종 답변 수정
→ dataset item 저장
→ 검수 완료 처리
→ JSONL export
```

## 채팅 실험 흐름

```txt
사용자 질문
→ 관련 기억 검색
→ 좋은 예시 일부 검색
→ 시스템 프롬프트 생성
→ /api/chat 요청
→ AI 제공자 호출
→ 답변 표시
→ 좋은 답변 저장 또는 실패 기록
```

## 현재 한계

- 서버 DB가 없어 브라우저별로 데이터가 분리된다.
- `app.js`에 화면 렌더링과 이벤트 로직이 많이 모여 있다.
- 기억 검색은 단순 텍스트 기반이다.
- 검수 상태가 아직 데이터 모델에 반영되지 않았다.
- 실제 파인튜닝 실행 기능은 없다.

## 확장 방향

- 데이터셋 검수 기능 추가
- 검수 완료 데이터만 export
- 기능별 모듈 분리
- RAG 또는 벡터 검색 추가
- 학습 전후 평가 기능 추가
