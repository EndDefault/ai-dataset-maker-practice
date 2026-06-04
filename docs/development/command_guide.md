# 명령어 가이드

명령어 예시는 Windows `cmd` 기준으로 작성한다.

## Git

```cmd
git status --short
git add README.md docs
git commit -m docs:init-project-docs
```

## Node

```cmd
node --check src\index.js
npm run start
```

## Python

```cmd
python --version
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 학습 스크립트 후보

```cmd
python training\validate_jsonl.py data\dataset.jsonl
python training\train_lora.py --dataset data\dataset.jsonl
python training\compare_lora.py --adapter training\output\adapter
```
