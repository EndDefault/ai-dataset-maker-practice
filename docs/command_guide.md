# 명령어 가이드

이 프로젝트의 명령어는 **Windows cmd 기준**으로 작성한다.

PowerShell 전용 명령어를 기본 실행 방법으로 사용하지 않는다.

## Python 환경

```cmd
python --version
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## SQLite 확인

현재 확인한 SQLite 버전은 3.49.1이다.

```cmd
python -c "import sqlite3; print(sqlite3.sqlite_version)"
```

## sqlite-vec 설치와 확인

`sqlite-vec`는 전역 설치하지 않고 프로젝트 가상환경에 설치한다.

```cmd
.venv\Scripts\activate
python -m pip install sqlite-vec
python -c "import sqlite3, sqlite_vec; db=sqlite3.connect(':memory:'); db.enable_load_extension(True); sqlite_vec.load(db); db.enable_load_extension(False); print(db.execute('select vec_version()').fetchone()[0])"
python -m pip freeze > requirements.txt
```

## Ollama 확인

```cmd
ollama list
ollama run qwen3:14b
```

## Ollama 모델 설치

RTX 5060 Ti 16GB 기준 기본 모델 세트다.

```cmd
ollama pull qwen3:14b
ollama pull qwen3:4b
ollama pull bge-m3
```

기존 모델을 정리할 때는 목록을 먼저 확인한 뒤 하나씩 삭제한다.

```cmd
ollama list
ollama rm model_name
```

## Streamlit 실행

```cmd
streamlit run app.py
```

## Git 확인

```cmd
git status --short
git diff --stat
```

## 주의

- 문서에는 `cmd`에서 실행 가능한 명령어를 우선 작성한다.
- Python 패키지는 프로젝트 `.venv`에 설치한다.
- 경로 예시는 Windows 스타일인 `uploads\sample.txt`를 사용한다.
- PowerShell 문법인 `Get-ChildItem`, `Set-Content`, `$env:` 같은 표현은 기본 문서에 쓰지 않는다.
