# 데이터 모델

## 저장 위치

현재 앱 상태는 브라우저 `localStorage`에 저장한다.

```txt
ai-maker-studio-state
```

앱은 `src/storage.js`에서 상태를 읽고 저장한다.

## 전체 상태 구조

현재 상태는 대략 다음 구조를 가진다.

```js
{
  profiles: [],
  activeProfileId: "profile-id",
  settings: {
    provider: "ollama",
    ollamaModel: "qwen2.5:7b",
    openaiModel: "gpt-4.1-mini"
  },
  dataset: [],
  failures: []
}
```

## Profile

AI 프로필은 AI의 역할과 말투를 정의한다.

```js
{
  id: "profile-id",
  name: "AI 이름",
  role: "역할",
  tone: "말투",
  personality: "성격",
  rules: "금지사항",
  style: "답변 스타일",
  memories: [],
  messages: []
}
```

## Memory

기억은 질문과 관련 있는 정보를 시스템 프롬프트에 넣기 위한 데이터다.

```js
{
  id: "memory-id",
  content: "기억 내용"
}
```

현재 관련 기억 검색은 단순 텍스트 기반이다. 데이터가 많아지면 키워드 점수화 또는 벡터 검색으로 확장할 수 있다.

## Chat Message

채팅 메시지는 역할과 내용을 가진다.

```js
{
  role: "user",
  content: "질문 내용"
}
```

```js
{
  role: "assistant",
  content: "AI 답변",
  provider: "ollama",
  model: "qwen2.5:7b"
}
```

## Dataset Item

학습 데이터 후보는 파인튜닝에 쓰기 쉬운 `messages` 배열을 가진다.

```js
{
  id: "dataset-id",
  profileId: "profile-id",
  profileName: "AI 이름",
  createdAt: "ISO 날짜 문자열",
  messages: [
    {
      role: "system",
      content: "시스템 프롬프트"
    },
    {
      role: "user",
      content: "사용자 질문"
    },
    {
      role: "assistant",
      content: "검수된 답변"
    }
  ]
}
```

## Failure Item

실패 기록은 모델과 프롬프트 개선에 쓰는 데이터다.

```js
{
  id: "failure-id",
  profileId: "profile-id",
  profileName: "AI 이름",
  createdAt: "ISO 날짜 문자열",
  userMessage: "사용자 질문",
  assistantMessage: "실패한 AI 답변",
  reason: "실패 이유"
}
```

## JSONL Export

현재 export는 `dataset` 배열의 각 항목에서 `messages`만 꺼내 한 줄씩 JSON으로 저장한다.

```jsonl
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
{"messages":[{"role":"system","content":"..."},{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
```

## 다음 데이터 구조 변경

검수 기능을 위해 `Dataset Item`에 다음 필드를 추가할 예정이다.

```js
{
  reviewStatus: "draft",
  reviewedAt: null,
  updatedAt: "ISO 날짜 문자열",
  source: "chat"
}
```

예상 상태값은 다음과 같다.

- `draft`: 저장은 되었지만 아직 검수 전
- `reviewed`: 사람이 확인했고 export 가능
- `rejected`: 학습 데이터로 쓰지 않음
