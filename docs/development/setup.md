# 설치와 실행

이 문서는 Windows `cmd` 기준으로 작성한다.

## 요구사항

- Git
- Node.js
- Python

## Node 실행 후보

```cmd
npm install
npm run start
```

또는 단순 서버라면:

```cmd
node server.js
```

## Python 환경 후보

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 주의

- PowerShell 전용 명령어를 기본 문서에 쓰지 않는다.
- 모델 파일과 학습 결과는 Git 추적에서 제외한다.
