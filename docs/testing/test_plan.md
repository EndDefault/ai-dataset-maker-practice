# 테스트 계획

## 테스트 범위

- JSON 구조 검증
- 필수 필드 검증
- 상태값 변경 검증
- JSONL export 검증
- 학습 스크립트 입력 검증
- UI 주요 흐름 검증

## 기본 테스트 케이스

- [ ] 빈 데이터는 저장되지 않는다.
- [ ] 필수 필드가 없으면 검사 실패한다.
- [ ] 잘못된 상태값은 거부된다.
- [ ] `reviewed` 데이터만 export된다.
- [ ] JSONL 한 줄은 `messages` 배열을 가진다.
- [ ] 학습 스크립트는 잘못된 JSONL을 거부한다.

## 검증 명령 후보

```cmd
node --check src\index.js
python training\validate_jsonl.py data\dataset.jsonl
```
