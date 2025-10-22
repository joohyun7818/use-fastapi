# 2단계: Poetry로 프로덕션 구조 재구성

> **목표**: 1단계에서 만든 프로젝트를 Poetry로 재구성하여 프로덕션급 의존성 관리 학습
>
> **학습 시간**: 2-3일
> **난이도**: ⭐⭐ (중간)
> **사전 요구사항**: 1단계 완료, Python 3.10+

---

## 📋 2단계 학습 목표

2단계를 완료하면 다음을 할 수 있게 됩니다:

- ✅ Poetry 설치 및 기본 사용법 이해
- ✅ `poetry new` 명령으로 프로젝트 생성
- ✅ `pyproject.toml` 파일 이해 및 관리
- ✅ 의존성 추가/제거 (`poetry add`, `poetry remove`)
- ✅ 가상환경 관리 (`poetry shell`, `poetry env`)
- ✅ 개발/프로덕션 의존성 분리
- ✅ 1단계 코드를 Poetry 프로젝트로 마이그레이션

**완료 시 결과물**: Poetry로 관리되는 프로덕션급 FastAPI 프로젝트

---

## 📚 2단계 목차

| 챕터                            | 주제                    | 예상 시간 |
| ------------------------------- | ----------------------- | --------- |
| [2.1](#21-poetry-이해하기)         | Poetry 이해하기         | 15분      |
| [2.2](#22-poetry-설치)             | Poetry 설치             | 10분      |
| [2.3](#23-새-poetry-프로젝트-생성) | 새 Poetry 프로젝트 생성 | 10분      |
| [2.4](#24-pyprojecttoml-이해)      | pyproject.toml 이해     | 20분      |
| [2.5](#25-의존성-추가)             | 의존성 추가             | 15분      |
| [2.6](#26-가상환경-관리)           | 가상환경 관리           | 15분      |
| [2.7](#27-1단계-코드-마이그레이션) | 1단계 코드 마이그레이션 | 30분      |
| [2.8](#28-프로덕션-폴더-구조)      | 프로덕션 폴더 구조      | 30분      |
| [2.9](#29-개발-의존성-관리)        | 개발 의존성 관리        | 20분      |
| [2.10](#210-스크립트-실행)         | 스크립트 실행           | 15분      |
| [2.11](#211-학습-체크리스트)       | 학습 체크리스트         | -         |

---

## 2.1 Poetry 이해하기

### Poetry란?

Poetry는 Python의 **의존성 관리 및 패키징 도구**입니다.

**Spring Boot의 Maven/Gradle과 유사한 역할**:

- Maven: `pom.xml` ↔ Poetry: `pyproject.toml`
- Gradle: `build.gradle` ↔ Poetry: `pyproject.toml`
- npm: `package.json` ↔ Poetry: `pyproject.toml`

### Poetry vs pip + requirements.txt

| 기능                         | pip + requirements.txt         | Poetry                         |
| ---------------------------- | ------------------------------ | ------------------------------ |
| **의존성 파일**        | requirements.txt (단순 목록)   | pyproject.toml (구조화된 설정) |
| **버전 관리**          | 수동으로 지정                  | 자동으로 해결                  |
| **잠금 파일**          | 없음 (수동으로 `pip freeze`) | poetry.lock (자동 생성)        |
| **가상환경**           | 별도로 `venv` 관리           | 자동으로 생성/관리             |
| **의존성 트리**        | 확인 어려움                    | `poetry show --tree`         |
| **프로덕션/개발 분리** | 별도 파일 필요                 | 내장 지원                      |

### Poetry의 장점

✅ **의존성 자동 해결**

- 패키지 간 충돌을 자동으로 해결
- 버전 제약사항 자동 관리

✅ **재현 가능한 빌드**

- `poetry.lock` 파일로 정확한 버전 기록
- 어디서나 동일한 환경 재현

✅ **개발/프로덕션 분리**

```bash
poetry add requests               # 프로덕션
poetry add --group dev pytest     # 개발용
```

✅ **가상환경 자동 관리**

- `poetry shell` 한 번으로 활성화
- 프로젝트별 독립적인 환경

✅ **Poetry 2.x의 향상된 성능**

- 더 빠른 의존성 해결
- 향상된 안정성 및 오류 처리
- 최신 Python 버전 지원 강화

---

## 2.2 Poetry 설치

### macOS에서 설치

**방법 1: Homebrew (권장)**

```bash
brew install poetry
```

**방법 2: 공식 설치 스크립트**

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 설치 확인

```bash
poetry --version
```

**예상 결과**:

```
Poetry (version 2.2.1)
```

### Poetry 설정 (선택)

프로젝트 폴더 내에 가상환경을 생성하도록 설정:

```bash
poetry config virtualenvs.in-project true
```

이 설정을 하면 `.venv` 폴더가 프로젝트 내부에 생성됩니다.

✅ **완료**: Poetry가 준비됐습니다!

---

## 2.3 새 Poetry 프로젝트 생성

### 중요: Poetry 2.2.1 기본값은 `src` 레이아웃입니다

Poetry 2.2.1부터 `poetry new`의 **기본값**이 `src` 레이아웃입니다:

```bash
poetry new kaira-fastapi-poetry
# 기본적으로 다음 구조가 생성됩니다 (src 레이아웃):
#
# kaira-fastapi-poetry/
# ├── src/
# │   └── kaira_fastapi_poetry/
# │       └── __init__.py
# ├── tests/
# ├── pyproject.toml
# ├── README.md
# └── poetry.lock
```

**`src` 레이아웃** (기본, 권장):

- 패키지가 `src/` 폴더 내에 위치
- 프로덕션 배포에 최적화
- 테스트와 소스 코드 분리

**`flat` 레이아웃** (선택):

- 패키지가 프로젝트 루트에 위치
- 작은 프로젝트에서 간편
- `poetry new --flat kaira-fastapi-poetry`로 생성

### poetry new 명령 실행

```bash
poetry new kaira-fastapi-poetry
cd kaira-fastapi-poetry
```

### 생성된 폴더 구조 확인 (src 레이아웃)

```bash
tree
# 또는 find 명령
find . -type f -o -type d | head -20
```

**예상 결과 (src 레이아웃 - Poetry 2.2 기본값)**:

```
kaira-fastapi-poetry/
├── pyproject.toml              # ← 프로젝트 설정 (중앙 설정 파일)
├── README.md                   # ← 프로젝트 설명
├── src/                        # ← 소스 폴더 (src 레이아웃 특징)
│   └── kaira_fastapi_poetry/   # ← 메인 패키지 (하이픈이 언더스코어로 변환됨)
│       └── __init__.py
└── tests/                      # ← 테스트 폴더
    └── __init__.py
```

**주요 파일/폴더 설명**:

| 항목                          | 설명                               | 용도                             |
| ----------------------------- | ---------------------------------- | -------------------------------- |
| `pyproject.toml`            | 프로젝트 메타데이터 및 의존성 설정 | Poetry의**중앙 설정 파일** |
| `src/`                      | 소스 코드 폴더 (src 레이아웃)      | 프로덕션 코드 분리               |
| `src/kaira_fastapi_poetry/` | 메인 패키지                        | 실제 애플리케이션 코드           |
| `tests/`                    | 테스트 폴더                        | 테스트 코드                      |
| `README.md`                 | 프로젝트 설명 문서                 | 프로젝트 소개                    |

**src 레이아웃의 장점**:

- ✅ 프로덕션 코드와 테스트 코드 분리
- ✅ 실수로 패키지 설치 전 import 방지
- ✅ 프로젝트 발행(PyPI) 시 권장 구조
- ✅ 프로펴셔널한 구조

### pyproject.toml 확인

```bash
cat pyproject.toml
```

**기본 내용**:

```toml
[tool.poetry]
name = "kaira-fastapi-poetry"
version = "0.1.0"
description = ""
authors = ["Your Name <you@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.10"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

✅ **완료**: Poetry 프로젝트 구조가 생성되었습니다!

---

## 2.4 pyproject.toml 이해

### pyproject.toml이란?

Python 프로젝트의 **중앙 설정 파일**입니다.

poetry로 생성한 프로젝트는 이 파일을 기준으로 하나의 프로젝트를 인식하여 관리합니다.

**역할**:

- 프로젝트 메타데이터 (이름, 버전, 작성자)
- 의존성 목록 (프로덕션 + 개발)
- 빌드 설정
- 도구 설정 (pytest, black 등)

### 주요 섹션 설명

#### `[tool.poetry]` - 프로젝트 정보

```toml
[tool.poetry]
name = "kaira-fastapi-poetry"        # 프로젝트 이름
version = "0.1.0"                    # 버전
description = "Kaira 웹사이트 서버"  # 설명
authors = ["Your Name <you@example.com>"]
readme = "README.md"
```

#### `[tool.poetry.dependencies]` - 프로덕션 의존성

```toml
[tool.poetry.dependencies]
python = "^3.10"      # Python 버전
fastapi = "^0.115.0"  # FastAPI
uvicorn = {extras = ["standard"], version = "^0.30.0"}
```

**버전 표기법**:

- `^0.115.0`: 0.115.0 이상, 1.0.0 미만 (호환 버전)
- `~0.115.0`: 0.115.0 이상, 0.116.0 미만 (마이너 버전)
- `==0.115.0`: 정확히 0.115.0
- `>=0.115.0`: 0.115.0 이상

#### `[tool.poetry.group.dev.dependencies]` - 개발 의존성

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^24.0.0"
flake8 = "^7.0.0"
```

#### `[build-system]` - 빌드 설정

```toml
[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

---

## 2.5 의존성 추가

### FastAPI와 Uvicorn 추가

```bash
poetry add fastapi "uvicorn[standard]"
```

**명령어 설명**:

- `poetry add`: 의존성 추가 명령
- `fastapi`: 패키지 이름
- `"uvicorn[standard]"`: uvicorn + 추가 기능 (WebSocket, HTTP/2)

**실행 과정**:

```
Using version ^0.115.0 for fastapi
Using version ^0.30.0 for uvicorn

Updating dependencies
Resolving dependencies... (1.2s)

Package operations: 25 installs, 0 updates, 0 removals

  • Installing annotated-types (0.7.0)
  • Installing anyio (4.11.0)
  • Installing certifi (2024.8.30)
  ...
  • Installing fastapi (0.115.0)
  • Installing uvicorn (0.30.0)

Writing lock file
```

### pyproject.toml 변경 확인

```bash
cat pyproject.toml
```

**변경된 내용**:

```toml
[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.30.0"}
```

### poetry.lock 파일 생성

```bash
ls -la poetry.lock
```

`poetry.lock` 파일이 자동으로 생성됩니다. 이 파일에는:

- 모든 의존성의 **정확한 버전**
- 각 패키지의 **해시값**
- 의존성 **트리 전체**

**중요**: `poetry.lock`을 Git에 커밋하세요! (재현 가능한 빌드를 위해)

### 다른 의존성 추가 예시

```bash
# 프로덕션 의존성 추가
poetry add requests

# 개발 의존성 추가
poetry add --group dev pytest

# 특정 버전 지정
poetry add fastapi==0.115.0

# 최신 버전 사용
poetry add fastapi@latest
```

---

## 2.6 가상환경 관리

### Poetry 가상환경 생성

Poetry는 프로젝트마다 자동으로 가상환경을 생성합니다.

```bash
poetry install
```

**실행 결과**:

```
Creating virtualenv kaira-fastapi-poetry in /Users/.../kaira-fastapi-poetry/.venv
Installing dependencies from lock file
...
Installing the current project: kaira-fastapi-poetry (0.1.0)
```

### 가상환경 진입

**방법 1: poetry env activate (권장)**

```bash
poetry env activate
```

**결과**:

```
Virtual environment already activated: /path/to/.venv
```

프롬프트가 `(.venv)` 또는 `(kaira-fastapi-poetry-py3.10)`으로 변경됩니다.

**나가기**:

```bash
exit
```

**방법 2: poetry run (일회성 명령)**

```bash
poetry run python --version
poetry run uvicorn main:app --reload
```

### 가상환경 정보 확인

```bash
poetry env info
```

**예상 결과**:

```
Virtualenv
Python:         3.10.12
Implementation: CPython
Path:           /Users/.../kaira-fastapi-poetry/.venv
Executable:     /Users/.../kaira-fastapi-poetry/.venv/bin/python
Valid:          True
```

### 가상환경 경로만 확인

```bash
poetry env info --path
```

**예상 결과**:

```
/Users/joohyun/joohyun/python/fast-api/kaira-fastapi-poetry/.venv
```

### 가상환경 삭제 및 재생성

```bash
# 현재 환경 삭제
poetry env remove python

# 또는 모든 환경 삭제
poetry env remove --all

# 재생성
poetry install
```

---

## 2.7 1단계 코드 마이그레이션

### 목표

1단계에서 작성한 `kaira-server/main.py`를 Poetry 프로젝트로 이동합니다.

### 1단계 코드 복사

```bash
# 현재 위치: kaira-fastapi-poetry/
cp ../kaira-server/main.py ./src/kaira_fastapi_poetry/main.py
cp ../kaira-server/kaira-1.0.0 ./src/kaira_fastapi_poetry/kaira-1.0.0
```

### main.py 내용 확인

```bash
cat src/kaira_fastapi_poetry/main.py
```

**내용**:

```python
									from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="Kaira Server",
    version="0.1.0",
    description="Kaira 웹사이트를 서빙하는 FastAPI 서버"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Kaira Server!", "status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "kaira-server"}

@app.get("/api/info")
def get_info():
    return {
        "name": "Kaira Server",
        "version": "0.1.0",
        "description": "정적 웹사이트 서빙 서버"
    }

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}"
    }

# 정적 파일 마운트
static_dir = Path(__file__).parent.parent / "kaira-1.0.0"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
```

### Poetry로 실행

```bash
poetry run uvicorn kaira_fastapi_poetry.main:app --reload
```

**명령어 설명**:

- `poetry run`: Poetry 가상환경에서 실행
- `kaira_fastapi_poetry.main:app`: 패키지명.모듈명:앱객체

**브라우저에서 확인**:

```
http://127.0.0.1:8000
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/health
```

✅ **성공**: 1단계 코드가 Poetry 프로젝트에서 작동합니다!

---

## 2.8 프로덕션 폴더 구조

### 권장 폴더 구조 (src 레이아웃 - Poetry 2.2.1 기본값)

Poetry 2.2.1에서 생성된 src 레이아웃의 프로덕션 구조입니다:

```
kaira-fastapi-poetry/
├── pyproject.toml                 # ← Poetry 설정 파일 (중앙)
├── poetry.lock                    # ← 의존성 잠금 파일
├── README.md
├── .gitignore
├── .env                           # ← 환경 변수 (추가 필요)
│
├── src/                           # ← src 레이아웃 특징 (분리된 소스 폴더)
│   └── kaira_fastapi_poetry/      # ← 메인 패키지
│       ├── __init__.py
│       ├── main.py                # ← FastAPI 앱 진입점
│       ├── config.py              # ← 환경 설정
│       │
│       ├── api/                   # ← API 라우터
│       │   ├── __init__.py
│       │   └── endpoints.py
│       │
│       └── utils/                 # ← 유틸리티 함수
│           ├── __init__.py
│           └── helpers.py
│
└── tests/                         # ← 테스트 (src 외부에 위치)
    ├── __init__.py
    ├── conftest.py                # ← pytest 설정
    └── test_main.py
```

**중요**: Poetry 2.2.1은 기본적으로 `src/` 폴더를 생성합니다.

- `poetry new kaira-fastapi-poetry` → src 레이아웃 (자동)
- `poetry new --flat kaira-fastapi-poetry` → flat 레이아웃 (명시적 옵션)

### 폴더 생성 (src 레이아웃)

```bash
# src 폴더 구조는 이미 생성되어 있습니다
# 추가 폴더/파일만 생성:

cd src/kaira_fastapi_poetry

# api 폴더 생성
mkdir -p api
touch api/__init__.py
touch api/endpoints.py

# utils 폴더 생성
mkdir -p utils
touch utils/__init__.py
touch utils/helpers.py

# config.py 생성
touch config.py
```

**또는 한 번에**:

```bash
mkdir -p src/kaira_fastapi_poetry/{api,utils}
touch src/kaira_fastapi_poetry/config.py
touch src/kaira_fastapi_poetry/api/{__init__.py,endpoints.py}
touch src/kaira_fastapi_poetry/utils/{__init__.py,helpers.py}
```

### config.py 작성

```python
# src/kaira_fastapi_poetry/config.py (src 레이아웃)
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """애플리케이션 설정 (pydantic-settings v2 최신 패턴)"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # .env 파일의 정의되지 않은 변수 무시
    )

    # 애플리케이션 메타정보
    app_name: str = Field(
        default="Kaira Server",
        description="애플리케이션 이름",
    )
    app_version: str = Field(
        default="0.1.0",
        description="애플리케이션 버전",
    )

    # 실행 환경 설정
    environment: str = Field(
        default="development",
        description="실행 환경 (development, staging, production)",
    )
    debug: bool = Field(
        default=True,
        description="디버그 모드 활성화 여부",
    )

    # 정적 파일 경로 (프론트엔드)
    static_files_path: str = Field(
        default="kaira-1.0.0",
        description="프론트엔드 정적 파일 폴더 경로 (src/kaira_fastapi_poetry/ 기준)",
    )


# 싱글톤 인스턴스 생성 (애플리케이션 전역에서 사용)
settings = Settings()
```

### api/endpoints.py 작성

```python
# src/kaira_fastapi_poetry/api/endpoints.py (src 레이아웃)
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "kaira-server"}

@router.get("/info")
def get_info():
    return {
        "name": "Kaira Server",
        "version": "0.1.0",
        "description": "정적 웹사이트 서빙 서버"
    }

@router.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}"
    }
```

### main.py 리팩토링

```python
# src/kaira_fastapi_poetry/main.py (src 레이아웃)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# src 레이아웃에서 모듈 import (importlib 사용 권장)
from kaira_fastapi_poetry.config import settings
from kaira_fastapi_poetry.api.endpoints import router as api_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Kaira 웹사이트를 서빙하는 FastAPI 서버"
)

# API 라우터 등록
app.include_router(api_router, prefix="/api", tags=["api"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Kaira Server!", "status": "ok"}

# 정적 파일 마운트 (config에서 경로 설정)
static_dir = Path(__file__).parent / settings.static_files_path
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print(f"⚠️  Warning: Static files not found at {static_dir}")
```

### pydantic-settings 추가

```bash
poetry add pydantic-settings
```

### 실행 및 테스트

```bash
poetry run uvicorn kaira_fastapi_poetry.main:app --reload
```

**브라우저에서 확인**:

```
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/api/info
http://127.0.0.1:8000/api/items/42
```

✅ **완료**: 프로덕션 구조로 리팩토링 완료!

---

## 2.9 개발 의존성 관리

### 개발 도구 추가

```bash
# 테스트 도구
poetry add --group dev pytest pytest-cov

# 코드 포맷터
poetry add --group dev black

# 린터
poetry add --group dev flake8

# 타입 체커
poetry add --group dev mypy
```

### pyproject.toml 확인

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^24.0.0"
flake8 = "^7.0.0"
mypy = "^1.0.0"
```

### 개발 의존성 제외하고 설치

프로덕션 환경에서는 개발 도구가 필요 없습니다:

```bash
poetry install --only main
```

또는:

```bash
poetry install --without dev
```

### 도구 설정 추가 (pyproject.toml - src 레이아웃 최적화)

```toml
[tool.black]
line-length = 88
target-version = ['py310']

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
pythonpath = "src"  # ← src 레이아웃에서 중요!
addopts = "--import-mode=importlib"  # ← importlib 모드 권장

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
mypy_path = "src"  # ← src 레이아웃 타입 체크
```

### 도구 실행

```bash
# 코드 포맷팅 (src 폴더 내용)
poetry run black src/kaira_fastapi_poetry/

# 린트 검사
poetry run flake8 src/kaira_fastapi_poetry/

# 타입 체크 (src 폴더)
poetry run mypy src/kaira_fastapi_poetry/

# 테스트 실행 (importlib 모드 자동 적용)
poetry run pytest tests/
```

---

## 2.10 스크립트 실행

### poetry run 사용

개별 명령 실행:

```bash
# src 레이아웃에서 모듈 실행
poetry run python -m kaira_fastapi_poetry.main

# FastAPI dev 서버 시작 (추천)
poetry run fastapi dev src/kaira_fastapi_poetry/main.py

# 또는 uvicorn 직접 실행
poetry run uvicorn kaira_fastapi_poetry.main:app --reload

# 테스트 실행
poetry run pytest tests/
```

### poetry shell 사용

쉘 진입 후 여러 명령 실행:

```bash
poetry shell

# 이제 poetry run 없이 실행 가능 (src 패키지 경로 자동 설정)
fastapi dev src/kaira_fastapi_poetry/main.py
pytest tests/
python -c "import fastapi; print(fastapi.__version__)"

# 나가기
exit
```

### 커스텀 스크립트 정의 (선택 - src 레이아웃)

`pyproject.toml`에 스크립트 추가:

```toml
[tool.poetry.scripts]
# src 레이아웃에서 모듈 지정
serve = "kaira_fastapi_poetry.main:app"
dev = "kaira_fastapi_poetry.main:main"
```

그 후:

```bash
poetry run serve
poetry run dev
```

### 의존성 목록 확인

```bash
# 모든 의존성 나열
poetry show

# 트리 형식으로
poetry show --tree

# 특정 패키지 정보
poetry show fastapi
```

### 의존성 업데이트

```bash
# 모든 의존성 업데이트
poetry update

# 특정 패키지만
poetry update fastapi

# 최신 버전 확인
poetry show --latest
```

---

## 2.11 학습 체크리스트

이 섹션을 완료했는지 확인하세요!

### 필수 체크리스트

- [ ] **Poetry 설치**

  - [ ] `poetry --version` 작동
  - [ ] Poetry 버전 1.8+ 설치됨
- [ ] **프로젝트 생성**

  - [ ] `poetry new` 명령으로 프로젝트 생성
  - [ ] `pyproject.toml` 파일 이해
  - [ ] `poetry.lock` 파일 생성됨
- [ ] **의존성 관리**

  - [ ] `poetry add` 로 FastAPI, Uvicorn 추가
  - [ ] `poetry add --group dev` 로 개발 도구 추가
  - [ ] `poetry show` 로 의존성 확인
- [ ] **가상환경**

  - [ ] `poetry shell` 로 환경 진입
  - [ ] `poetry env info` 로 정보 확인
  - [ ] `poetry run` 으로 명령 실행
- [ ] **코드 마이그레이션**

  - [ ] 1단계 코드를 Poetry 프로젝트로 이동
  - [ ] `poetry run uvicorn` 으로 실행 성공
  - [ ] 모든 엔드포인트 정상 작동
- [ ] **프로덕션 구조**

  - [ ] `api/`, `utils/` 폴더 생성
  - [ ] `config.py` 작성
  - [ ] 라우터 분리 완료

### 심화 체크리스트 (선택)

- [ ] `.env` 파일로 환경 변수 관리
- [ ] `poetry export` 로 requirements.txt 생성
- [ ] `poetry build` 로 패키지 빌드
- [ ] 커스텀 스크립트 정의

### 마지막 확인

**아래 명령을 모두 성공적으로 실행했나요?**

```bash
# 1. Poetry로 프로젝트 생성
poetry new kaira-fastapi-poetry
cd kaira-fastapi-poetry

# 2. 의존성 추가
poetry add fastapi "uvicorn[standard]"
poetry add --group dev pytest black

# 3. 코드 작성 및 실행
poetry run uvicorn kaira_fastapi_poetry.main:app --reload

# 4. 테스트
poetry run pytest tests/

# 5. 의존성 확인
poetry show --tree
```

✅ **모두 성공하면 2단계 완료입니다!**

---

## 📖 다음 단계

2단계를 완료했으면 준비가 됐습니다!

**다음 선택지:**

- **→ 3단계로 진행**: `03_TESTING_LOGGING_GUIDE.md` 읽기

  - 테스트 코드 작성
  - 에러 핸들링
  - 로깅 시스템
- **→ 2단계 심화**: Poetry 고급 기능

  - 플러그인 시스템
  - 프라이빗 저장소
  - 패키지 퍼블리싱

---

## 🎯 2단계 정리

| 항목              | 학습 내용                                                        |
| ----------------- | ---------------------------------------------------------------- |
| **도구**    | Poetry                                                           |
| **명령어**  | `poetry new`, `poetry add`, `poetry shell`, `poetry run` |
| **개념**    | 의존성 관리, 가상환경, pyproject.toml, poetry.lock               |
| **파일**    | pyproject.toml, poetry.lock                                      |
| **구조**    | 프로덕션급 폴더 구조                                             |
| **배운 점** | Poetry로 일관성 있고 재현 가능한 환경 구축!                      |

---

## ✨ 축하합니다

2단계 완료! 이제 Poetry로 프로덕션급 프로젝트 관리를 마스터했습니다. 🚀
