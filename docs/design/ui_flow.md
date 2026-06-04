# UI 흐름

## 페이지 구조

```txt
Main
→ Text Translation
→ Image Translation
→ Review Workspace
→ Reference Library
```

## Main

- 번역 작업 상태 요약
- 다음 작업 표시
- 주요 페이지 이동

## Text Translation

- 영어 원문 입력
- 초벌 번역 확인
- 정규화 번역 확인
- 최종 번역 수정
- 번역 작업 저장

## Image Translation

- 이미지 업로드
- 번역할 텍스트 영역 지정
- crop 이미지 저장
- OCR 실행
- OCR 결과 수정과 승인

## Review Workspace

- OCR 검수 대기 목록
- 번역 검수 대기 목록
- 최종 번역 수정
- 승인/거절 처리

## Reference Library

- 용어집 추가
- 이전 번역 검색
- 문체 규칙 저장
- 번역 중 참고 자료 확인
