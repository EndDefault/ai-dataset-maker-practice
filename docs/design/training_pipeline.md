# 학습 파이프라인

## 목표

검수된 지도학습 데이터셋을 PyTorch/PEFT 기반 LoRA 학습으로 연결한다.

## 기본 흐름

```txt
reviewed 후보 선택
→ JSONL export
→ JSONL validation
→ 베이스 모델 로드
→ LoRA 설정 적용
→ 학습 실행
→ adapter 저장
→ 원본 모델과 LoRA 모델 비교
→ 실험 로그 작성
```

## 사용 후보

- Python
- PyTorch
- Hugging Face Transformers
- Datasets
- PEFT
- Accelerate

## 첫 실험 기준

- 작은 모델부터 시작한다.
- 데이터는 20~50개로 흐름 검증을 먼저 한다.
- 목표는 품질보다 학습 파이프라인 작동 확인이다.

## cmd 기준 명령 예시

```cmd
python training\validate_jsonl.py data\dataset.jsonl
python training\train_lora.py --dataset data\dataset.jsonl --model Qwen/Qwen2.5-0.5B-Instruct
python training\compare_lora.py --adapter training\output\adapter
```

## 실험 기록 항목

- 베이스 모델
- 데이터 개수
- 학습 step 또는 epoch
- LoRA rank
- learning rate
- batch size
- 실행 시간
- 오류 여부
- 학습 전후 비교
- 한계와 다음 실험
