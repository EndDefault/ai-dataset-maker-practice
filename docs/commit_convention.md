# 커밋 규칙

이 규칙은 앞으로 계속 사용한다.

## 메시지 형식

공백 없는 짧은 제목을 우선한다.

```txt
docs:reset-mvp-plan
feat:add-command-router
feat:add-summary-task
feat:add-search-task
feat:add-error-analysis
fix:handle-empty-command
refactor:split-task-modules
test:add-summary-sample
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

## 커밋 전 확인

```cmd
git status --short
git diff --stat
```

## 첫 MVP docs 커밋 예시

```cmd
git add README.md docs
git commit -m docs:reset-mvp-plan
```

## 원칙

- 기능 단위로 작게 커밋한다.
- 문서와 구현이 함께 바뀌면 같은 커밋에 넣을 수 있다.
- 서로 다른 목적의 변경은 커밋을 나눈다.
- 대용량 모델 파일, 가상환경, 실행 결과 캐시는 Git에 넣지 않는다.
