# Local AI Training Workbench

로컬 환경에서 지도학습용 데이터셋을 만들고, 검수하고, PyTorch/PEFT 기반 LoRA 학습과 결과 비교까지 이어가기 위한 AI 학습 워크벤치다.

## 현재 단계

이 저장소는 docs-first 방식으로 다시 시작한다. 코드를 만들기 전에 프로젝트 목표, 데이터 모델, 학습 파이프라인, RAG 역할, 커밋 규칙을 먼저 고정한다.

## 핵심 방향

- 대형 모델 없이도 사람이 통제 가능한 학습 데이터셋을 만든다.
- 데이터 후보는 JSON으로 관리하고, 최종 학습 데이터는 JSONL로 export한다.
- 확실한 검사는 코드가 맡고, 애매한 평가는 나중에 검사 AI 또는 사람 검수로 보완한다.
- 학습은 PyTorch, Transformers, PEFT 기반 LoRA를 우선한다.
- RAG는 모델을 학습시키는 대신 참고 문서와 기존 예시를 찾는 보조 장치로 사용한다.

## 문서

시작점은 [docs/index.md](docs/index.md)다.
