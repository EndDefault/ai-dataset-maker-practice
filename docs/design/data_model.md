# 데이터 모델

## Training Project

```json
{
  "id": "project-001",
  "name": "nabi-tone",
  "purpose": "짧고 자연스러운 냥체 답변 습관을 학습한다.",
  "baseModel": "Qwen/Qwen2.5-0.5B-Instruct",
  "targetCount": 100,
  "createdAt": "",
  "updatedAt": ""
}
```

## Dataset Candidate

```json
{
  "id": "candidate-001",
  "projectId": "project-001",
  "status": "draft",
  "stage": "generated",
  "input": {
    "topic": "LoRA가 필요한 이유",
    "facts": [
      "프롬프트 참고만으로 모델 자체가 바뀌지는 않는다.",
      "LoRA는 말투와 출력 습관 조정에 적합하다."
    ],
    "intent": "초보자에게 짧게 설명"
  },
  "output": {
    "system": "너는 짧고 자연스러운 냥체 답변 데이터를 만든다.",
    "user": "LoRA가 왜 필요해?",
    "assistant": "프롬프트만으로는 모델 습관이 바뀌지 않는다냥. LoRA는 말투나 답변 형식을 모델에 더 가깝게 익히게 할 때 쓴다냥."
  },
  "checks": {
    "jsonValid": true,
    "requiredFieldsPassed": true,
    "forbiddenWordsPassed": true,
    "sentenceCountPassed": true,
    "messagesPassed": true
  },
  "issues": [],
  "metadata": {
    "source": "manual",
    "createdAt": "",
    "updatedAt": ""
  }
}
```

## 상태값

| 상태 | 의미 |
| --- | --- |
| `draft` | 생성됨 |
| `checked` | 코드 검사 통과 |
| `needs_revision` | 수정 필요 |
| `revised` | 수정 완료 |
| `polished` | 다듬기 완료 |
| `reviewed` | 사람이 학습 데이터로 승인 |
| `rejected` | 사용하지 않음 |

## 학습용 JSONL

최종 학습 파일은 `reviewed` 후보만 아래 구조로 export한다.

```json
{"messages":[{"role":"system","content":""},{"role":"user","content":""},{"role":"assistant","content":""}]}
```

## 저장 원칙

- 후보 데이터는 내부 관리용 JSON으로 저장한다.
- 학습에는 JSONL export 결과만 사용한다.
- 검사 결과와 이슈는 후보 JSON에 남긴다.
- 대용량 모델 파일과 adapter는 Git에 넣지 않는다.
