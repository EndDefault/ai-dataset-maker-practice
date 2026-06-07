# ai-dataset-maker-practice

로컬 LLM과 RAG 구조를 연습하기 위한 프로젝트다.

완성형 서비스나 고성능 RAG 제품을 목표로 하기보다, **AI를 활용해 로컬 문서 질의응답 앱을 만들고, 실행하고, 평가하고, 한계를 기록하는 과정**을 익히는 데 목적을 둔다.

## 현재 상태

1차 구현은 여기서 마무리한다.

현재 앱은 Streamlit 기반 로컬 작업 콘솔로 동작한다. 사용자는 txt/md/pdf 파일을 업로드하고, 문서를 chunk로 나눈 뒤, 로컬 Ollama 모델을 사용해 문서 기반 질문을 실행할 수 있다.

현재 기준에서 되는 것:

- txt/md/pdf 파일 업로드
- PDF 텍스트 추출 가능 여부 확인
- 문서 chunk 생성
- chunk를 SQLite에 저장
- `bge-m3`로 문서 chunk와 질문 embedding 생성
- `sqlite-vec` 기반 벡터 검색
- 벡터 검색 실패 시 lexical fallback 검색
- `qwen3:14b`로 RAG 답변 생성
- Markdown 결과와 실행 기록 저장
- RAG 평가 스크립트 실행

현재 기준에서 아직 부족한 것:

- 스캔 PDF OCR
- PDF/표/복잡한 문서 파싱 품질
- RAG 답변의 의미적 정확도 보장
- 깊은 평가 기준
- `qwen3:4b` 기반 입력 정제 AI 연결
- 정교한 UI/UX 설계

즉, 이 프로젝트는 **RAG가 완성됐다**기보다 **RAG를 테스트하고 개선할 수 있는 기본 구조를 만들었다**고 보는 것이 맞다.

## 기술 구성

| 영역 | 사용 기술 |
| --- | --- |
| UI | Streamlit |
| 로컬 LLM | Ollama |
| 답변 생성 모델 | `qwen3:14b` |
| 입력 정제 후보 모델 | `qwen3:4b` |
| 임베딩 모델 | `bge-m3` |
| DB | SQLite |
| 벡터 검색 | `sqlite-vec` |
| 결과 저장 | Markdown, SQLite |
| 평가 | `evals/rag/run_eval.py` |

## RAG 흐름

```txt
문서 업로드
→ 텍스트 추출
→ chunk 생성
→ bge-m3 embedding 생성
→ SQLite / sqlite-vec 저장
→ 질문 입력
→ 질문 embedding 생성
→ 관련 chunk 검색
→ qwen3:14b에 근거와 질문 전달
→ Markdown 답변 생성
```

중요한 점은 이 프로젝트가 모델을 새로 학습시키는 `train` 방식이 아니라는 것이다. 문서를 모델에 학습시키는 대신, 질문할 때 관련 문서 조각을 찾아서 모델에 함께 넣는 RAG 방식이다.

## 실행 방법

Windows `cmd` 기준:

```cmd
.venv\Scripts\activate
streamlit run app.py
```

브라우저에서 아래 주소를 연다.

```txt
http://127.0.0.1:8501
```

## 평가 실행

RAG 기본 동작 점검:

```cmd
.venv\Scripts\python.exe evals\rag\run_eval.py --dry-run
.venv\Scripts\python.exe evals\rag\run_eval.py
```

현재 평가 스크립트는 성능을 깊게 보장하는 용도가 아니라, RAG 실행 흐름이 깨지지 않았는지 확인하는 기준선이다.

마지막 확인 기준으로는 5개 평가 케이스가 모두 통과했다. 다만 이는 “기본 실행과 얕은 검증이 통과했다”는 의미이며, 답변 품질 자체는 별도 검토가 필요하다.

## 문서

시작점은 [docs/index.md](docs/index.md)다.

핵심 문서:

- [docs/project-status.md](docs/project-status.md): 현재 상태와 1차 종료 기준
- [docs/ai-collaboration.md](docs/ai-collaboration.md): AI 활용 방식과 배운 점
- [docs/architecture.md](docs/architecture.md): 전체 구조와 RAG/DB 흐름
- [docs/command_guide.md](docs/command_guide.md): 실행 명령어
- [evals/rag/README.md](evals/rag/README.md): RAG 평가 스크립트 설명

## 이 프로젝트의 의미

이 프로젝트는 “AI가 대신 만들어준 결과물”이라기보다, AI를 활용해 개발 과정을 나누고 검토한 연습 기록이다.

특히 다음을 확인했다.

- AI에게 막연히 요청하면 불필요한 결과가 섞인다.
- UI는 기능보다 먼저 정보 우선순위와 규격이 필요하다.
- RAG는 모델 성능보다 문서 파싱, chunk 품질, 검색 품질이 먼저 흔들린다.
- 자동 평가는 완성도 보장이 아니라 문제를 발견하기 위한 기준선이다.
- AI를 잘 쓰려면 요구사항, 검토 기준, 삭제할 것까지 명확히 말해야 한다.

1차 목표는 여기까지로 정리하고, 다음 단계에서는 문서 파싱 품질, 평가 기준, UI 설계 규칙을 더 치밀하게 다룬다.
