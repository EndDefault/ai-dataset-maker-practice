# 아키텍처

## 전체 구조

```txt
UI
→ Local API
→ File Storage
→ Dataset Pipeline
→ Training Pipeline
→ Experiment Lab
→ Reference Library
```

## 구성 요소

| 영역 | 역할 |
| --- | --- |
| UI | 데이터 후보, 검사 결과, 학습 결과를 조작 |
| Local API | 파일 저장, 검사, 학습 스크립트 실행 연결 |
| File Storage | 프로젝트, 후보 데이터, 실험 로그 저장 |
| Dataset Pipeline | 생성, 검사, 수정, 다듬기, 승인 |
| Training Pipeline | JSONL 검증, LoRA 학습, adapter 저장 |
| Experiment Lab | 원본 모델과 학습 모델 비교 |
| Reference Library | RAG용 참고 문서 저장과 검색 |

## 기본 데이터 흐름

```txt
프로젝트 정의
→ 데이터 후보 JSON
→ 코드 검사
→ 사람 검수
→ reviewed JSONL export
→ PyTorch/PEFT LoRA 학습
→ adapter 저장
→ 원본 모델과 비교
→ 실험 로그 기록
```

## 우선순위

1. 데이터 후보 구조와 저장
2. 코드 검사와 reviewed export
3. LoRA 학습 스크립트
4. 실험 비교
5. RAG 참고 자료 연결
