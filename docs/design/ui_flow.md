# UI 흐름

## 페이지 구조

```txt
Main
→ Dataset Builder
→ Dataset Inspector
→ Training Lab
→ Experiment Lab
→ Reference Library
```

## Main

- 프로젝트 상태 요약
- 다음 작업 표시
- 주요 페이지 이동

## Dataset Builder

- 프로젝트 선택
- 데이터 후보 JSON 작성
- 입력 정보와 출력 문장 관리
- 후보 저장

## Dataset Inspector

- 코드 검사 실행
- 검사 결과와 이슈 확인
- 상태값 변경
- reviewed/rejected 처리

## Training Lab

- reviewed 데이터 개수 확인
- JSONL export
- validation 실행
- LoRA 학습 실행
- adapter 결과 경로 확인

## Experiment Lab

- 테스트 질문 목록 관리
- 원본 모델 답변 기록
- LoRA 모델 답변 기록
- 차이와 한계 기록

## Reference Library

- RAG용 문서 추가
- 문서 검색 테스트
- 데이터 후보 생성 시 참고할 자료 확인
