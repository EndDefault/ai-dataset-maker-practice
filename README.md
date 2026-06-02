# AI Maker Studio

AI를 바로 학습시키기 전에, AI 프로필과 기억을 만들고 좋은 답변을 데이터셋으로 모으는 연습용 MVP입니다.

## 기능별 구조

- `server.js`: 화면 파일을 제공하고, `/api/chat`에서 선택한 AI 제공자에 연결합니다.
- `src/index.js`: 앱 진입점입니다. 화면 이벤트를 연결하고 전체 상태를 렌더링합니다.
- `src/core/promptBuilder.js`: 프로필과 기억을 합쳐서 시스템 프롬프트를 만듭니다.
- `src/core/storage.js`: 브라우저 `localStorage`에 데이터를 저장하고 JSONL 파일을 내려받습니다.
- `src/features/profiles/profiles.js`: AI 이름, 역할, 말투, 성격 같은 프로필을 만듭니다.
- `src/features/memories/memories.js`: 사용자가 넣은 기억을 저장하고, 질문과 관련 있는 기억을 찾습니다.
- `src/features/chat/chat.js`: 브라우저에서 로컬 서버의 `/api/chat`으로 메시지를 보냅니다.
- `src/features/dataset/dataset.js`: 좋은 답변을 파인튜닝에 쓰기 좋은 `messages` 형태로 바꿉니다.

## Ollama로 무료 연습하기

Ollama는 API 키가 아니라 내 컴퓨터의 로컬 서버에 연결합니다.

1. 모델을 설치합니다.

```cmd
ollama pull qwen2.5:7b
```

컴퓨터가 부담스러우면 더 작은 모델을 써도 됩니다.

```cmd
ollama pull qwen2.5:3b
```

2. Ollama 서버가 실행 중인지 확인합니다.

```cmd
ollama serve
```

Ollama 앱이 이미 켜져 있으면 이 명령은 따로 필요 없을 수 있습니다.

3. 이 앱의 서버를 실행합니다.

```cmd
npm start
```

또는:

```cmd
node server.js
```

4. 브라우저에서 엽니다.

```txt
http://localhost:5173
```

기본 제공자는 `Ollama 로컬`, 기본 모델은 `qwen2.5:7b`입니다. 화면의 설정 탭에서 설치한 모델 이름으로 바꿀 수 있습니다.

## 제공자 선택

설정 탭의 `AI 연결`에서 선택할 수 있습니다.

- `Ollama 로컬`: 무료. 내 컴퓨터의 `http://localhost:11434`에 연결합니다.
- `연습용 가짜 답변`: 모델 없이 화면과 데이터 저장 흐름만 테스트합니다.
- `OpenAI API`: 유료 API입니다. 이 모드를 쓰려면 `OPENAI_API_KEY`가 필요합니다.

OpenAI를 쓸 때만 Command Prompt에서 키를 설정합니다.

```cmd
set OPENAI_API_KEY=여기에_API_키
npm start
```

## 현재 단계

현재 앱은 다음 흐름을 연습합니다.

```txt
AI 프로필 만들기
→ 기억 추가하기
→ 프로필과 기억을 AI에게 같이 보내기
→ AI 답변 받기
→ 좋은 답변 저장하기 또는 직접 수정해서 저장하기
→ 실패 이유 기록하기
→ JSONL로 내보내기
```

이 방식은 모델을 바로 학습시키는 것이 아니라, 좋은 답변을 모아 나중에 학습 데이터로 쓰기 위한 준비 단계입니다.

## 다음 단계의 의미

작은 로컬 모델은 답변이 흔들릴 수 있으므로, 이제부터는 AI 답변을 그대로 믿는 것이 아니라 사람이 검수합니다.

- `좋은 답변 저장`: 그대로 학습 데이터 후보에 넣습니다.
- `수정해서 저장`: 사람이 고친 답변을 학습 데이터 후보에 넣습니다.
- `실패 기록`: 왜 실패했는지 기록해서 모델과 프롬프트 개선에 사용합니다.
