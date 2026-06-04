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

## OCR/번역 스크립트 후보

```cmd
python ocr\extract_region_text.py data\crops\region-001.png
node --check src\index.js
```
