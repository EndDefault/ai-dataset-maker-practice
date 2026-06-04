# 커밋 규칙

커밋은 기능 단위로 작게 남긴다.

## 메시지 형식

공백 없는 짧은 제목을 우선한다.

```txt
docs:init-project-docs
feat:add-dataset-builder
fix:validate-json-output
refactor:split-training-pipeline
test:add-jsonl-validation
experiment:first-lora-run
```

## 타입

| 타입 | 의미 |
| --- | --- |
| `docs` | 문서 변경 |
| `feat` | 기능 추가 |
| `fix` | 버그 수정 |
| `refactor` | 동작 유지 구조 변경 |
| `test` | 테스트 추가/수정 |
| `chore` | 설정, 정리 |
| `data` | 데이터셋 변경 |
| `experiment` | 실험 기록 또는 실험 스크립트 |

## 첫 커밋

```cmd
git add README.md docs
git commit -m docs:init-project-docs
```

## 커밋 전 확인

```cmd
git status --short
git diff --stat
```

## 원칙

- 서로 다른 목적의 변경은 커밋을 나눈다.
- 문서와 구현이 함께 바뀌면 같은 커밋에 넣을 수 있다.
- 실험 결과는 조건과 결과 문서를 함께 커밋한다.
- 생성된 대용량 모델 파일은 Git에 넣지 않는다.
