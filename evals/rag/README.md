# RAG evals

이 폴더는 RAG 답변 품질을 반복해서 점검하기 위한 평가 세트다.

`train` 데이터가 아니라 `evals`다. 모델을 학습시키는 목적이 아니라, 현재 RAG 검색과 답변이 같은 질문에서 어떻게 변하는지 기록한다.

## 파일

```txt
evals/rag/
  cases.json       평가 질문 목록
  run_eval.py      평가 실행 스크립트
  reports/         실행 결과 리포트가 생성되는 폴더
```

## 실행

프로젝트 루트에서 실행한다.

```cmd
.venv\Scripts\python.exe evals\rag\run_eval.py
```

실제 모델 호출 없이 케이스와 입력 문서만 확인한다.

```cmd
.venv\Scripts\python.exe evals\rag\run_eval.py --dry-run
```

일부 케이스만 실행한다.

```cmd
.venv\Scripts\python.exe evals\rag\run_eval.py --limit 3
```

## 케이스 작성 기준

- `question`: 실제 Home에서 입력할 자연어 질문
- `input_paths`: 기본값은 `uploads`
- `checks.min_sources`: 최소 근거 chunk 수
- `checks.expected_terms`: 답변 Markdown에 포함되면 좋은 단어
- `checks.forbidden_terms`: 답변에 나오면 안 되는 단어

자동 평가는 답변 품질을 완전히 판단하지 않는다. 리포트의 답변과 sources를 보고 실패 유형을 따로 적는다.
