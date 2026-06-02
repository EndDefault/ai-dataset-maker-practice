# AI Maker Studio 현재 상태

이 문서는 지금까지 무엇을 만들었고, 프로젝트가 어느 단계에 있는지 정리한 기록이다.

## 프로젝트 목표

최종 목표는 내가 원하는 말투와 규칙을 따르는 AI를 만들기 위한 학습 데이터 제작 도구를 만드는 것이다.

현재 앱은 모델을 바로 학습시키는 도구가 아니다. 질문, 핵심 사실, 원하는 말투를 바탕으로 학습 데이터 후보를 만들고 JSONL로 내보내는 준비 도구다.

## 현재 만든 것

### 1. 기본 화면 구조

- 왼쪽: AI 프로필 목록
- 가운데: 채팅 화면
- 오른쪽: 설정, 기억, 제작, 데이터 탭
- 채팅 입력창은 아래에 고정
- 채팅 메시지 영역만 스크롤

### 2. AI 프로필 기능

- AI 이름 설정
- 역할 설정
- 말투 설정
- 성격 설정
- 금지사항 설정
- 답변 스타일 설정
- 설정을 바탕으로 시스템 프롬프트 생성

### 3. 기억 기능

- 기억 추가
- 기억 삭제
- 질문과 관련 있는 기억 일부를 찾아 시스템 프롬프트에 포함

### 4. AI 연결 기능

- `practice`: 비용 없이 테스트하는 가짜 답변 모드
- `ollama`: 로컬 Ollama 서버 연결
- `openai`: OpenAI API 연결
- 기본 제공자는 `ollama`
- 기본 Ollama 모델은 `qwen2.5:7b`

### 5. 답변 저장 기능

- AI 답변을 좋은 답변으로 저장
- AI 답변을 직접 수정해서 저장
- 실패 이유 기록
- 중국어 한자가 섞인 답변은 좋은 예시 저장을 막음

### 6. 데이터 제작 탭

- 질문 입력
- 핵심 사실 입력
- 원하는 말투와 형식 입력
- AI가 초안 생성
- 사람이 최종 답변 수정
- 수정된 최종 답변을 학습 데이터 후보로 저장

### 7. 데이터 관리 기능

- 좋은 예시 목록 표시
- 실패 기록 목록 표시
- 저장된 좋은 예시 수정
- 저장된 좋은 예시 삭제
- JSONL export
- 데이터 비우기
- 앱 전체 초기화

### 8. 큐레이션 데이터셋

- 직접 검수한 `나비` 기준 좋은 예시 50개 생성
- `scripts/create-curated-state.js`로 `data/app-state.json` 재생성 가능
- 생성된 dataset source는 `curated`
- `ai-maker-dataset.jsonl` export 결과 50줄 확인
- 각 줄은 `system`, `user`, `assistant` 메시지 구조
- 현재 50개 데이터는 1차 LoRA 실험용 기준 데이터셋

### 9. 문서화

- `README.md`: 실행 방법과 기능 설명
- `docs/index.md`: 문서 목록과 갱신 규칙
- `docs/planning/requirements.md`: 요구사항 명세
- `docs/planning/checklist.md`: 단계별 개발 체크리스트
- `docs/planning/portfolio-direction.md`: 포트폴리오 관점의 문제 정의, 구조, 데이터 흐름, 한계, 개선 방향 정리
- `docs/planning/decision_log.md`: 중요한 의사결정과 이유
- `docs/planning/refactor_plan.md`: 리팩터링 순서와 기준
- `docs/design/architecture.md`: 전체 아키텍처와 데이터 흐름
- `docs/design/data.md`: 데이터 모델과 JSONL 구조
- `docs/design/ui_index.md`: 주요 화면과 UI 구성
- `docs/design/src_structure.md`: `src` 폴더 구조 정리 계획
- `docs/development/seed_data.md`: 초기 데이터와 테스트 데이터 설계
- `docs/development/curated_dataset.md`: 50개 큐레이션 데이터 생성 방식
- `docs/development/lora_plan.md`: LoRA 실험 계획과 현재 환경 확인
- `docs/development/commit_convention.md`: 커밋 메시지 규칙과 기능 단위 커밋 기준
- `docs/testing/test_plan.md`: 테스트 전략과 케이스
- `docs/testing/test_result.md`: 테스트 실행 결과
- `docs/logs/implementation_log.md`: 구현 이력과 설계 결정
- `docs/logs/bugfix_log.md`: 버그 수정 기록
- `docs/reference/glossary.md`: 용어와 핵심 로직 공부 노트
- `practice/ai-learning-flow.md`: AI 학습 흐름 정리
- `practice/data-making-next-step.md`: 답변 생성에서 데이터 제작으로 방향을 바꾼 이유 정리

## 지금까지 알게 된 점

- 작은 로컬 모델은 비용 없이 실험하기 좋다.
- 하지만 말투 유지, 사실 정확도, 긴 답변 안정성은 약하다.
- 특히 모델이 모르는 내용을 그럴듯하게 말하는 할루시네이션 문제가 있다.
- 그래서 AI에게 정답을 맡기기보다, 사람이 핵심 사실을 제공하고 AI는 문장 초안만 만들게 하는 방향이 더 안전하다.
- 저장된 데이터는 앱 안에 저장되고 JSONL로 내보낼 수 있지만, 모델 자체가 바로 학습되는 것은 아니다.
- 50개 좋은 예시를 프롬프트에 참고시켜도 모델 자체가 바뀌는 것은 아니다.
- 현재 방식은 파인튜닝이 아니라 프롬프트 참고 방식이므로, 중국어 섞임이나 냥체 누락 같은 한계가 남는다.
- 원하는 말투를 모델 자체에 더 가깝게 반영하려면 LoRA 실험이 다음 단계다.

## 현재 단계

현재 프로젝트는 `1차 데이터셋 제작 완료, LoRA 실험 준비` 단계다.

완료된 단계:

```txt
AI 프로필 실험
→ 기억 기능 실험
→ Ollama 연결
→ 모델 한계 확인
→ 데이터 제작 탭 추가
→ 수정된 답변을 학습 데이터 후보로 저장
→ 저장된 좋은 예시 수정/삭제 기능 추가
→ 직접 검수한 큐레이션 데이터 50개 생성
→ JSONL export 50줄 정상 확인
```

아직 하지 않은 단계:

```txt
검수 완료 데이터만 export
데이터 100개 제작
LoRA 학습 환경 설치
작은 모델로 LoRA 1회 학습
학습 전후 답변 비교
```

## 다음에 할 일

추천 다음 단계는 LoRA 1차 실험 준비다.

- 현재 JSONL을 학습용 포맷으로 한 번 더 검증
- RTX 3050 8GB 기준으로 작은 모델 선택
- 처음은 `Qwen2.5 0.5B` 또는 `Qwen2.5 1.5B` LoRA가 안전
- Python 학습 환경에 `torch`, `transformers`, `datasets`, `peft`, `accelerate` 설치
- 1회 짧은 LoRA 학습 실행
- 같은 질문 10개로 학습 전후 비교

포트폴리오 관점에서는 `docs/planning/portfolio-direction.md`와 `docs/planning/decision_log.md`를 계속 업데이트한다. 구현이 바뀔 때마다 문제 정의, 구조, 데이터 흐름, 한계, 다음 개선 방향도 같이 수정한다.

데이터를 더 늘릴 때는 현재 50개 기준을 유지하면서 100개까지 확장한다.

현재 실험 말투 후보:

```txt
자연스러운 냥체
존댓말 금지
"합니다냥", "있습니다냥", "생각해요냥" 같은 어색한 표현 금지
"다냥", "한다냥", "좋다냥" 같은 끝맺음 사용
3문장 이내
핵심 사실에 없는 내용 추가 금지
```

## 한 문장 요약

지금 만든 것은 AI를 바로 학습시킨 결과물이 아니라, 사람이 통제한 사실과 말투를 바탕으로 LoRA 실험에 넣을 1차 데이터셋 50개를 만든 로컬 AI 데이터 제작 도구다.
