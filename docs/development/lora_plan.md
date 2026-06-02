# LoRA 실험 계획

## 현재 결론

현재 앱에서 50개 좋은 예시를 프롬프트에 넣는 방식은 파인튜닝이 아니다. 모델 자체가 학습된 것이 아니므로, Ollama 기본 모델은 여전히 중국어를 섞거나 냥체를 놓치거나 예시를 어색하게 따라 할 수 있다.

`ai-maker-dataset.jsonl`은 학습이 끝난 결과물이 아니라 LoRA 학습에 넣을 1차 데이터셋이다. 1차 실험에서는 이 50개 데이터로 `Qwen2.5 0.5B` LoRA adapter 생성까지 확인했다.

## 현재 확인한 환경

- Python: `3.12.10`
- GPU: NVIDIA GeForce RTX 3050 8GB
- Ollama 모델: `qwen2.5:3b`, `qwen2.5:7b`
- JSONL 데이터: 50줄
- JSONL 구조: 각 줄이 `system`, `user`, `assistant` 메시지를 포함
- 학습 패키지: `.venv`에 `torch`, `transformers`, `datasets`, `peft`, `accelerate` 설치 확인
- 1차 결과: `training/output/qwen2.5-0.5b-nabi-lora/adapter_model.safetensors` 생성 확인

## 1차 실험 결과

목표는 완벽한 모델을 만드는 것이 아니라 다음을 확인하는 것이었다.

- JSONL 데이터가 학습에 들어가는가
- LoRA 어댑터가 생성되는가
- 학습 전후 같은 질문에서 말투와 답변 길이가 달라지는가
- 50개 데이터만으로 어떤 한계가 남는가

확인 결과:

- JSONL 50개 구조 검증 통과
- `Qwen/Qwen2.5-0.5B-Instruct` 다운로드와 로드 확인
- 20 step 짧은 LoRA 학습 실행
- adapter 파일 생성 확인
- 원본 모델과 LoRA adapter 적용 모델의 출력 차이 확인

## 다음 권장 실험

처음부터 7B로 가지 않는다. RTX 3050 8GB에서는 7B LoRA도 부담이 클 수 있으므로, 1차 실험은 작은 모델로 학습 흐름을 확인한다.

추천 순서:

```txt
Qwen2.5 0.5B LoRA
→ Qwen2.5 1.5B LoRA
→ 가능하면 Qwen2.5 3B LoRA
```

## 예상 흐름

```txt
1. 학습 환경 설치
2. JSONL 데이터 검증
3. 학습용 스크립트 작성
4. 작은 모델로 짧은 LoRA 학습 실행
5. 어댑터 저장
6. 학습 전후 질문 10개 비교
7. 결과와 한계를 docs에 기록
```

## 주의할 점

- Ollama는 주로 모델 실행 도구이고, 파인튜닝 도구가 아니다.
- LoRA 학습은 Hugging Face 모델과 Python 학습 라이브러리로 진행하는 것이 일반적이다.
- 학습 결과를 Ollama에서 쓰려면 병합 또는 변환 과정이 추가로 필요할 수 있다.
- 50개 데이터는 실험용으로 충분하지만, 안정적인 말투를 기대하려면 100개 이상으로 늘리는 것이 좋다.

## 다음 작업 후보

- 학습 결과와 한계 문서화
- LoRA 프로젝트와 템플릿 기반 데이터 생성 방향 구체화
- 목적별 데이터셋을 100개 이상으로 확장
- LoRA adapter 병합과 Ollama 등록 흐름 조사
