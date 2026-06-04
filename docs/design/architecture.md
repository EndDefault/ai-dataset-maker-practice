# 아키텍처

## 전체 구조

```txt
UI
→ Local API
→ File Storage
→ Image/OCR Pipeline
→ Translation Pipeline
→ Review Workspace
→ Reference Library
```

## 구성 요소

| 영역 | 역할 |
| --- | --- |
| UI | 원문, OCR 결과, 번역 결과, 상태를 조작 |
| Local API | 파일 저장, OCR 실행, 번역 요청 연결 |
| File Storage | 원본 이미지, crop 이미지, 번역 작업 JSON 저장 |
| Image/OCR Pipeline | 영역 지정, crop 저장, OCR 추출, OCR 검수 |
| Translation Pipeline | 초벌 번역, 정규화, 최종 번역 검수 |
| Review Workspace | OCR과 번역 상태 확인, 수정, 승인 |
| Reference Library | 용어집, 이전 번역, 문체 규칙 검색 |

## 기본 데이터 흐름

```txt
텍스트 입력 또는 이미지 업로드
→ 이미지라면 영역 지정과 crop 저장
→ OCR 텍스트 추출
→ OCR 결과 수정과 승인
→ 초벌 번역
→ 정규화 번역
→ 최종 번역 수정과 승인
→ 번역 작업 JSON 저장
```

## 우선순위

1. 텍스트 번역 작업 구조와 저장
2. 번역 상태값 관리
3. 이미지 영역 지정과 crop 저장
4. PaddleOCR 연동
5. RAG 참고 자료 연결
