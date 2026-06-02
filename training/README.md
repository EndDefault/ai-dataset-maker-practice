# LoRA 1차 실행 확인

이 폴더는 완성 모델을 만들기보다, 현재 JSONL 데이터로 LoRA 학습 파이프라인이 실제로 도는지 확인하기 위한 최소 구성이다.

## 목표

- `messages` JSONL 구조 검증
- 작은 Qwen 모델로 짧은 LoRA 학습 실행
- LoRA adapter 저장 확인

## 데이터 준비

다운로드한 파일을 다음 위치에 둔다.

```txt
training/data/ai-maker-dataset.jsonl
```

현재 사용 중인 파일 예시:

```txt
C:/Users/YJU/Downloads/ai-maker-dataset.jsonl
```

## 환경 설치

Python 3.12에서는 일부 학습 패키지 조합이 불편할 수 있다. 가능하면 Python 3.10 또는 3.11 가상환경을 권장한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r training/requirements.txt
```

CUDA용 PyTorch가 자동으로 맞지 않으면 PyTorch 공식 안내에 맞춰 CUDA 버전을 지정해서 다시 설치한다.

## 데이터 검증

```powershell
python training/validate_jsonl.py training/data/ai-maker-dataset.jsonl
```

## 짧은 LoRA 학습 실행

외부 모델 다운로드 없이 코드 경로만 확인하려면 smoke test를 먼저 실행한다.

```powershell
python training/smoke_lora.py --data training/data/ai-maker-dataset.jsonl --output training/output/smoke-lora --max-steps 3
```

이 smoke test는 실제 Qwen 모델이 아니라 아주 작은 임시 모델을 코드에서 만들어 사용한다. 따라서 결과물은 실사용 모델이 아니고, LoRA 학습 루프와 adapter 저장 확인용이다.

처음에는 20 step 정도만 돌려서 adapter 생성 여부를 확인한다.

```powershell
python training/train_lora.py --data training/data/ai-maker-dataset.jsonl --output training/output/qwen2.5-0.5b-nabi-lora --max-steps 20
```

성공하면 다음 폴더에 adapter 파일이 저장된다.

```txt
training/output/qwen2.5-0.5b-nabi-lora
```

## 학습 전후 비교

```cmd
python training\compare_lora.py --adapter training\output\qwen2.5-0.5b-nabi-lora
```

이 명령은 같은 질문을 원본 모델과 LoRA adapter를 붙인 모델에 각각 보내고 답변을 비교한다.

## 기대치

50개 데이터는 실험용으로 충분하지만, 안정적인 말투 모델을 기대하기에는 적다. 이번 목표는 성능보다 다음 세 가지 확인이다.

- 학습 코드가 실행되는가
- GPU 메모리가 버티는가
- LoRA adapter가 저장되는가
