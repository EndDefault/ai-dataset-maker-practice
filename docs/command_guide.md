# 명령어 가이드

이 프로젝트의 명령어는 **Windows cmd 기준**으로 작성한다.

PowerShell 전용 명령어를 기본 실행 방법으로 사용하지 않는다.

## Python 환경

```cmd
python --version
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Streamlit 실행

```cmd
streamlit run app.py
```

## Ollama 확인

```cmd
ollama list
ollama run qwen2.5:7b
```

## Git 확인

```cmd
git status --short
git diff --stat
```

## 주의

- 문서에는 `cmd`에서 실행 가능한 명령어를 우선 작성한다.
- 경로 예시는 Windows 스타일인 `uploads\sample.txt`를 사용한다.
- PowerShell 문법인 `Get-ChildItem`, `Set-Content`, `$env:` 같은 표현은 기본 문서에 쓰지 않는다.
