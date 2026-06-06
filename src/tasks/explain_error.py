from __future__ import annotations

from src.config import get_config
from src.errors import AppError
from src.schemas import TaskRequest
from src.tasks.common import generate_korean_checked, success_result


def run(request: TaskRequest):
    config = get_config()
    prompt = f"""다음 에러 메시지를 분석해 주세요.

출력 형식:
1. 에러 의미
2. 가능한 원인
3. 확인할 파일
4. 수정 예시
5. 재발 방지 체크리스트

에러 메시지:
{request.command}
"""
    try:
        answer = generate_korean_checked(prompt, model=config.main_model, task_name="에러 분석")
    except AppError as error:
        answer = fallback_error_explanation(request.command, error.message)
    return success_result(request, title="에러 분석", body=answer, model=config.main_model)


def fallback_error_explanation(message: str, reason: str) -> str:
    return f"""Ollama 호출을 사용할 수 없어 기본 분석 템플릿을 표시합니다.

원인: {reason}

## 에러 메시지

```txt
{message}
```

## 확인 순서

- 에러가 발생한 파일과 줄 번호를 확인한다.
- 최근 변경한 import, 패키지 설치, 설정 파일을 확인한다.
- 같은 이름의 모듈이나 클래스가 중복되어 있는지 확인한다.
- 재현 명령과 전체 로그를 저장한다.
"""
