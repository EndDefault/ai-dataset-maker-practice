# Gitmoji 커밋 규칙

이 프로젝트는 Gitmoji 기반 커밋 메시지를 사용한다.

## 기본 형식

커밋 제목은 아래 형식을 사용한다.

```txt
<깃모지> <작업 분류> : <작업 내용>
```

예시:

```cmd
git commit -m "✨ 기능 추가 : 로그인 기능 추가"
git commit -m "🐛 버그 수정 : 로그인 실패 오류 수정"
git commit -m "💄 UI 수정 : 마이페이지 사이드바 개선"
git commit -m "♻️ 리팩토링 : 계정관리 모달 로직 분리"
git commit -m "📝 문서 수정 : README 실행 방법 추가"
```

## 상세 설명

커밋 제목만으로 부족하면 두 번째 메시지에 한 줄 상세 설명을 붙인다.

```cmd
git commit -m "✨ 기능 추가 : 로그인 기능 추가" -m "이메일과 비밀번호 입력, 검증, 로그인 성공 후 이동 흐름을 추가했다."
```

상세 설명은 무엇을 바꿨는지 한 줄로 적는다.

좋은 예시:

```cmd
git commit -m "🧱 구조 변경 : UI 폴더 구조 정리" -m "Streamlit UI를 app, features, shared 구조로 나누는 기준을 문서화했다."
```

## 자주 쓰는 Gitmoji

| Gitmoji | 코드 | 작업 분류 | 의미 |
| --- | --- | --- | --- |
| ✨ | `:sparkles:` | 기능 추가 | 새 기능 추가 |
| 🐛 | `:bug:` | 버그 수정 | 오류 수정 |
| 💄 | `:lipstick:` | UI 수정 | UI, 스타일 수정 |
| ♻️ | `:recycle:` | 리팩토링 | 동작 유지 구조 개선 |
| 📝 | `:memo:` | 문서 수정 | 문서 추가/수정 |
| ✅ | `:white_check_mark:` | 테스트 | 테스트 추가/수정 |
| 🔥 | `:fire:` | 삭제 | 코드/파일 삭제 |
| 🎨 | `:art:` | 구조 개선 | 코드 구조, 포맷 개선 |
| ⚡️ | `:zap:` | 성능 개선 | 성능 개선 |
| 🚑️ | `:ambulance:` | 긴급 수정 | 긴급 버그 수정 |
| 🚀 | `:rocket:` | 배포 | 배포 관련 변경 |
| 🎉 | `:tada:` | 초기 설정 | 프로젝트 시작/초기화 |
| 🔧 | `:wrench:` | 설정 수정 | 설정 파일 수정 |
| 🔨 | `:hammer:` | 빌드 수정 | 개발 스크립트, 빌드 수정 |
| 📦 | `:package:` | 패키지 수정 | 패키지, 의존성 수정 |
| 🔒️ | `:lock:` | 보안 수정 | 보안 관련 수정 |
| 🚚 | `:truck:` | 파일 이동 | 파일 이동, 이름 변경 |
| 🚧 | `:construction:` | 작업 중 | 아직 완료되지 않은 작업 |
| 💥 | `:boom:` | 큰 변경 | breaking change |
| 🗃️ | `:card_file_box:` | DB 수정 | DB, schema, migration 수정 |
| 🧱 | `:bricks:` | 구조 변경 | 인프라, 폴더 구조, 큰 뼈대 변경 |
| 🔌 | `:electric_plug:` | API 연동 | 외부 API, 모델 호출, 연동 코드 |
| 🔗 | `:link:` | 연결 | 링크, 라우팅, 네비게이션 연결 |

## 이 프로젝트 추천 예시

문서:

```cmd
git commit -m "📝 문서 수정 : 로컬 AI 실행 기준 정리" -m "모델, SQLite, RAG, UI 구조 결정 내용을 docs에 반영했다."
git commit -m "📝 문서 수정 : Gitmoji 커밋 규칙 정리" -m "커밋 형식, 작업 분류, 상세 설명 작성 규칙을 추가했다."
```

구조:

```cmd
git commit -m "🧱 구조 변경 : 기본 폴더 구조 추가" -m "src, data, uploads, outputs, tests 디렉터리 뼈대를 생성했다."
git commit -m "🧱 구조 변경 : UI 폴더 구조 추가" -m "Streamlit UI를 app, features, shared 구조로 분리했다."
```

모델/API:

```cmd
git commit -m "🔌 API 연동 : Ollama 호출 클라이언트 추가" -m "qwen3 모델 호출을 위한 공통 클라이언트를 구현했다."
git commit -m "🔌 API 연동 : bge-m3 임베딩 호출 추가" -m "RAG 검색용 문서 chunk embedding 생성 흐름을 추가했다."
```

DB/RAG:

```cmd
git commit -m "🗃️ DB 수정 : 실행 기록 테이블 추가" -m "runs, artifacts, errors 테이블 초기 migration을 작성했다."
git commit -m "🗃️ DB 수정 : 벡터 검색 저장소 추가" -m "sqlite-vec 기반 chunk embedding 저장 구조를 추가했다."
```

UI:

```cmd
git commit -m "💄 UI 수정 : 작업 콘솔 화면 추가" -m "명령 입력, 실행 상태, 결과 미리보기 영역을 구성했다."
git commit -m "🔗 연결 : Streamlit 페이지 네비게이션 추가" -m "Home, Documents, Runs, Settings 페이지 이동을 연결했다."
```

테스트:

```cmd
git commit -m "✅ 테스트 : 작업 JSON 검증 테스트 추가" -m "입출력 정제 결과가 schema를 만족하는지 확인하는 테스트를 추가했다."
```

## 커밋 전 확인

```cmd
git status --short
git diff --stat
```

## 커밋 순서

모든 파일을 한 번에 넣기보다 목적별로 나눈다.

```cmd
git add docs
git commit -m "📝 문서 수정 : Gitmoji 커밋 규칙 정리" -m "커밋 형식, 작업 분류, 상세 설명 작성 규칙을 추가했다."
```

특정 파일만 커밋할 때:

```cmd
git add docs\commit_convention.md
git commit -m "📝 문서 수정 : Gitmoji 커밋 규칙 정리" -m "프로젝트에서 사용할 Gitmoji 커밋 형식을 문서화했다."
```

## 원칙

- 커밋 제목은 `<깃모지> <작업 분류> : <작업 내용>` 형식을 사용한다.
- 상세 설명은 필요할 때 한 줄로 추가한다.
- 가능하면 기능, 문서, 설정, DB 변경을 나눠 커밋한다.
- 커밋 메시지만 보고 무엇을 바꿨는지 알 수 있어야 한다.
- 대용량 모델 파일, 가상환경, 실행 결과 캐시는 Git에 넣지 않는다.
