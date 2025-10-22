# 3단계: 테스트와 로깅 완벽 가이드

## 📚 3단계 목차

| 챕터 | 주제 | 예상 시간 |
|------|------|---------|
| [3.1](#31-학습-목표) | 학습 목표 | - |
| [3.2](#32-pytest-이해하기) | Pytest 이해하기 | 30분 |
| [3.3](#33-fastapi-testclient) | FastAPI TestClient | 45분 |
| [3.4](#34-테스트-코드-작성) | 테스트 코드 작성 | 1시간 |
| [3.5](#35-에러-처리) | 에러 처리 | 45분 |
| [3.6](#36-로깅-시스템) | 로깅 시스템 | 1시간 |
| [3.7](#37-환경-변수-관리) | 환경 변수 관리 | 30분 |
| [3.8](#38-테스트-커버리지) | 테스트 커버리지 | 45분 |
| [3.9](#39-실전-예제) | 실전 예제 | 1시간 |
| [3.10](#310-문제-해결) | 문제 해결 | 30분 |
| [3.11](#311-체크리스트) | 체크리스트 | - |

---

## 3.1 학습 목표

이 단계를 완료하면 다음을 할 수 있습니다:

✅ **테스트 프레임워크**
- pytest 기본 사용법 이해
- FastAPI TestClient로 API 테스트 작성
- Fixture와 Parametrize 활용

✅ **에러 처리**
- HTTPException으로 표준 에러 반환
- 커스텀 예외 핸들러 구현
- 검증 에러 커스터마이징

✅ **로깅**
- Python logging 모듈 활용
- 요청/응답 로깅 구현
- 로그 레벨과 포맷 관리

✅ **설정 관리**
- pydantic-settings로 환경 변수 관리
- .env 파일 활용
- 개발/운영 환경 분리

✅ **테스트 커버리지**
- pytest-cov로 커버리지 측정
- 테스트 리포트 생성

**예상 소요 시간**: 4-6시간

---

## 3.2 Pytest 이해하기

### 3.2.1 Pytest란?

Pytest는 Python에서 가장 널리 사용되는 테스트 프레임워크입니다.

**주요 특징**:
- 간결한 문법 (`assert` 문만으로 테스트)
- 강력한 fixture 시스템
- 플러그인 생태계 풍부
- 자동 테스트 검색
- 상세한 실패 리포트

### 3.2.2 Pytest 설치

```bash
# 기본 pytest 설치
pip install pytest

# 커버리지 측정 도구 포함
pip install pytest pytest-cov

# 모든 테스트 도구 설치 (권장)
pip install pytest pytest-cov pytest-asyncio
```

**설치 확인**:
```bash
pytest --version
```

### 3.2.3 첫 번째 테스트 작성

**테스트 파일 구조**:
```
kaira-server/
├── app/
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py
```

**간단한 테스트 예제** (`tests/test_main.py`):
```python
# tests/test_main.py
def test_addition():
    """덧셈 테스트"""
    assert 1 + 1 == 2

def test_string():
    """문자열 테스트"""
    result = "hello world"
    assert result.startswith("hello")
    assert "world" in result
    assert len(result) == 11
```

**테스트 실행**:
```bash
# 모든 테스트 실행
pytest

# 특정 파일 실행
pytest tests/test_main.py

# 특정 테스트 함수 실행
pytest tests/test_main.py::test_addition

# 상세 출력 (-v: verbose)
pytest -v

# 실패한 테스트만 다시 실행
pytest --lf
```

### 3.2.4 Pytest Fixture

Fixture는 테스트에 필요한 데이터나 환경을 준비하는 함수입니다.

**기본 Fixture**:
```python
# tests/test_fixtures.py
import pytest

@pytest.fixture
def sample_data():
    """테스트에서 사용할 샘플 데이터"""
    return {"name": "홍길동", "age": 30}

def test_sample_data(sample_data):
    """fixture 사용 예제"""
    assert sample_data["name"] == "홍길동"
    assert sample_data["age"] == 30
```

**Fixture Scope**:
```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="function")
def function_fixture():
    """각 테스트마다 실행 (기본값)"""
    print("\n함수 fixture 시작")
    yield "function data"
    print("\n함수 fixture 종료")

@pytest.fixture(scope="module")
def module_fixture():
    """모듈당 한 번만 실행"""
    print("\n모듈 fixture 시작")
    yield "module data"
    print("\n모듈 fixture 종료")

@pytest.fixture(scope="session")
def session_fixture():
    """전체 테스트 세션당 한 번 실행"""
    print("\n세션 fixture 시작")
    yield "session data"
    print("\n세션 fixture 종료")
```

### 3.2.5 Parametrize (매개변수화)

여러 입력값으로 같은 테스트를 실행할 수 있습니다.

**기본 예제**:
```python
# tests/test_parametrize.py
import pytest

@pytest.mark.parametrize("input,expected", [
    ("3+5", 8),
    ("2+4", 6),
    ("10-5", 5),
])
def test_eval(input, expected):
    """매개변수화 테스트"""
    assert eval(input) == expected
```

**여러 매개변수 조합**:
```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    """모든 조합 테스트 (4개 테스트 생성)"""
    assert x < y
```

---

## 3.3 FastAPI TestClient

### 3.3.1 TestClient 이해하기

FastAPI의 `TestClient`는 실제 서버 없이 API를 테스트할 수 있게 해줍니다.

**특징**:
- 실제 HTTP 요청 없이 테스트 (메모리 내 실행)
- 동기식 테스트 작성 가능 (async/await 불필요)
- 모든 HTTP 메서드 지원 (GET, POST, PUT, DELETE 등)
- 헤더, 쿠키, 파일 업로드 테스트 가능

### 3.3.2 기본 사용법

**간단한 FastAPI 앱** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**TestClient로 테스트** (`tests/test_main.py`):
```python
# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """루트 경로 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    """아이템 조회 테스트"""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}
```

### 3.3.3 POST 요청 테스트

```python
# app/main.py에 추가
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created"}
```

```python
# tests/test_main.py에 추가
def test_create_item():
    """아이템 생성 테스트"""
    response = client.post(
        "/items/",
        json={"name": "책", "price": 15000, "is_offer": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["item"]["name"] == "책"
    assert data["item"]["price"] == 15000
    assert data["message"] == "Item created"
```

### 3.3.4 헤더와 쿠키 테스트

```python
# app/main.py에 추가
from fastapi import Header

@app.get("/headers/")
async def read_headers(
    user_agent: str = Header(None),
    x_token: str = Header(None)
):
    return {
        "User-Agent": user_agent,
        "X-Token": x_token
    }
```

```python
# tests/test_main.py에 추가
def test_headers():
    """헤더 전송 테스트"""
    response = client.get(
        "/headers/",
        headers={
            "User-Agent": "TestClient",
            "X-Token": "secret-token"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["User-Agent"] == "TestClient"
    assert data["X-Token"] == "secret-token"
```

### 3.3.5 Fixture로 TestClient 재사용

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="module")
def test_client():
    """모든 테스트에서 재사용할 TestClient"""
    with TestClient(app) as client:
        yield client

# tests/test_main.py 수정
def test_read_root(test_client):
    """fixture 사용"""
    response = test_client.get("/")
    assert response.status_code == 200
```

---

## 3.4 테스트 코드 작성

### 3.4.1 테스트 디렉토리 구조

```
kaira-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── items.py
│   │   └── users.py
│   └── utils.py
└── tests/
    ├── __init__.py
    ├── conftest.py              # 전역 fixture
    ├── test_main.py             # 메인 앱 테스트
    ├── test_routers/
    │   ├── __init__.py
    │   ├── test_items.py
    │   └── test_users.py
    └── test_utils.py
```

### 3.4.2 정적 파일 서빙 테스트

**앱 코드** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# 정적 파일 마운트
static_path = Path(__file__).parent.parent / "kaira-1.0.0"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def root():
    return {"message": "Kaira Static Server"}
```

**테스트 코드** (`tests/test_static.py`):
```python
# tests/test_static.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Kaira Static Server"}

def test_static_html_file():
    """정적 HTML 파일 접근 테스트"""
    response = client.get("/static/index.html")
    
    # 파일이 존재하면 200, 없으면 404
    if response.status_code == 200:
        assert "text/html" in response.headers["content-type"]
        assert len(response.content) > 0
    else:
        assert response.status_code == 404

def test_static_css_file():
    """정적 CSS 파일 접근 테스트"""
    response = client.get("/static/style.css")
    
    if response.status_code == 200:
        assert "text/css" in response.headers["content-type"]
```

### 3.4.3 데이터 검증 테스트

**Pydantic 모델** (`app/models.py`):
```python
# app/models.py
from pydantic import BaseModel, Field, validator

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
    
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('이름은 공백일 수 없습니다')
        return v.strip()
```

**검증 테스트** (`tests/test_models.py`):
```python
# tests/test_models.py
import pytest
from pydantic import ValidationError
from app.models import Item

def test_item_valid():
    """올바른 데이터 검증"""
    item = Item(name="책", price=15000, quantity=3)
    assert item.name == "책"
    assert item.price == 15000
    assert item.quantity == 3

def test_item_invalid_price():
    """잘못된 가격 검증"""
    with pytest.raises(ValidationError) as exc_info:
        Item(name="책", price=-1000)
    
    errors = exc_info.value.errors()
    assert any(err['loc'] == ('price',) for err in errors)

def test_item_empty_name():
    """빈 이름 검증"""
    with pytest.raises(ValidationError) as exc_info:
        Item(name="   ", price=1000)
    
    assert "이름은 공백일 수 없습니다" in str(exc_info.value)

@pytest.mark.parametrize("name,price,should_pass", [
    ("책", 1000, True),
    ("", 1000, False),
    ("책", 0, False),
    ("책", -100, False),
    ("A" * 51, 1000, False),  # 너무 긴 이름
])
def test_item_validation(name, price, should_pass):
    """매개변수화 검증 테스트"""
    if should_pass:
        item = Item(name=name, price=price)
        assert item.name == name.strip()
    else:
        with pytest.raises(ValidationError):
            Item(name=name, price=price)
```

---

## 3.5 에러 처리

### 3.5.1 HTTPException 사용

**기본 에러 처리** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI, HTTPException

app = FastAPI()

items_db = {"item1": "책", "item2": "펜"}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )
    return {"item_id": item_id, "name": items_db[item_id]}
```

**에러 테스트** (`tests/test_errors.py`):
```python
# tests/test_errors.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_existing_item():
    """존재하는 아이템 조회"""
    response = client.get("/items/item1")
    assert response.status_code == 200
    assert response.json()["name"] == "책"

def test_get_nonexistent_item():
    """존재하지 않는 아이템 조회"""
    response = client.get("/items/item999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
```

### 3.5.2 커스텀 헤더가 있는 에러

```python
# app/main.py에 추가
@app.get("/items-header/{item_id}")
async def get_item_with_header(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "Custom error header"}
        )
    return {"item_id": item_id, "name": items_db[item_id]}
```

```python
# tests/test_errors.py에 추가
def test_error_with_custom_header():
    """커스텀 헤더가 있는 에러"""
    response = client.get("/items-header/item999")
    assert response.status_code == 404
    assert "X-Error" in response.headers
    assert response.headers["X-Error"] == "Custom error header"
```

### 3.5.3 커스텀 예외 핸들러

```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class ItemNotFoundException(Exception):
    """커스텀 예외: 아이템을 찾을 수 없음"""
    def __init__(self, item_id: str):
        self.item_id = item_id

app = FastAPI()

@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    """커스텀 예외 핸들러"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "ItemNotFound",
            "message": f"아이템 '{exc.item_id}'를 찾을 수 없습니다",
            "suggestion": "아이템 ID를 확인해주세요"
        }
    )

@app.get("/custom-items/{item_id}")
async def get_custom_item(item_id: str):
    if item_id not in items_db:
        raise ItemNotFoundException(item_id)
    return {"item_id": item_id, "name": items_db[item_id]}
```

```python
# tests/test_errors.py에 추가
def test_custom_exception():
    """커스텀 예외 핸들러 테스트"""
    response = client.get("/custom-items/item999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "ItemNotFound"
    assert "item999" in data["message"]
    assert "suggestion" in data
```

### 3.5.4 검증 에러 커스터마이징

```python
# app/main.py에 추가
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """검증 에러 커스터마이징"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "입력 데이터가 올바르지 않습니다",
            "details": errors
        }
    )

from pydantic import BaseModel

class CreateItem(BaseModel):
    name: str
    price: float

@app.post("/validated-items/")
async def create_validated_item(item: CreateItem):
    return {"item": item}
```

```python
# tests/test_errors.py에 추가
def test_validation_error():
    """검증 에러 커스터마이징 테스트"""
    response = client.post(
        "/validated-items/",
        json={"name": "책", "price": "invalid"}  # 잘못된 타입
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "details" in data
    assert len(data["details"]) > 0
```

---

## 3.6 로깅 시스템

### 3.6.1 Python logging 기본

**로깅 설정** (`app/logging_config.py`):
```python
# app/logging_config.py
import logging
import sys
from pathlib import Path

def setup_logging():
    """로깅 설정"""
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 로그 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    
    # 루트 로거 설정
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # 콘솔 출력
            logging.StreamHandler(sys.stdout),
            # 파일 출력
            logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        ]
    )
    
    # 특정 로거 레벨 조정
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# 로거 생성 함수
def get_logger(name: str):
    """로거 인스턴스 생성"""
    return logging.getLogger(name)
```

**메인 앱에서 사용** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI
from app.logging_config import setup_logging, get_logger

# 로깅 설정
setup_logging()
logger = get_logger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """앱 시작 시 실행"""
    logger.info("애플리케이션 시작")

@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 시 실행"""
    logger.info("애플리케이션 종료")

@app.get("/")
async def root():
    logger.info("루트 경로 접근")
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    logger.info(f"아이템 조회 요청: {item_id}")
    try:
        # 아이템 조회 로직
        result = {"item_id": item_id, "name": f"Item {item_id}"}
        logger.debug(f"아이템 조회 성공: {result}")
        return result
    except Exception as e:
        logger.error(f"아이템 조회 실패: {e}", exc_info=True)
        raise
```

### 3.6.2 로그 레벨

```python
# app/examples/logging_levels.py
from app.logging_config import get_logger

logger = get_logger(__name__)

def demonstrate_log_levels():
    """로그 레벨 예제"""
    
    # DEBUG: 상세한 디버깅 정보
    logger.debug("디버그 메시지 - 개발 중에만 필요")
    
    # INFO: 일반 정보
    logger.info("정보 메시지 - 정상 동작 기록")
    
    # WARNING: 경고 (문제는 아니지만 주의 필요)
    logger.warning("경고 메시지 - 잠재적 문제 발견")
    
    # ERROR: 에러 (기능 실패)
    logger.error("에러 메시지 - 기능 실행 실패")
    
    # CRITICAL: 치명적 에러 (앱 중단 위험)
    logger.critical("치명적 에러 - 앱이 계속 실행 불가능")
```

**환경별 로그 레벨 설정**:
```python
# app/logging_config.py 수정
import os

def setup_logging():
    # 환경 변수로 로그 레벨 결정
    env = os.getenv("ENVIRONMENT", "development")
    
    if env == "production":
        log_level = logging.WARNING  # 운영: WARNING 이상만
    elif env == "staging":
        log_level = logging.INFO     # 스테이징: INFO 이상
    else:
        log_level = logging.DEBUG    # 개발: 모든 로그
    
    logging.basicConfig(
        level=log_level,
        # ... 나머지 설정
    )
```

### 3.6.3 미들웨어로 요청/응답 로깅

```python
# app/middleware/logging.py
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """요청/응답 로깅 미들웨어"""
    # 요청 시작 시간
    start_time = time.time()
    
    # 요청 정보 로깅
    logger.info(f"요청 시작: {request.method} {request.url.path}")
    logger.debug(f"요청 헤더: {dict(request.headers)}")
    
    # 요청 처리
    response = await call_next(request)
    
    # 처리 시간 계산
    process_time = time.time() - start_time
    
    # 응답 정보 로깅
    logger.info(
        f"요청 완료: {request.method} {request.url.path} "
        f"- 상태: {response.status_code} - 시간: {process_time:.3f}초"
    )
    
    # 응답 헤더에 처리 시간 추가
    response.headers["X-Process-Time"] = str(process_time)
    
    return response
```

**미들웨어 등록** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI
from app.middleware.logging import log_requests

app = FastAPI()

# 미들웨어 등록
app.middleware("http")(log_requests)

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 3.6.4 로깅 테스트

```python
# tests/test_logging.py
import logging
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_request_logging(caplog):
    """요청 로깅 테스트 (pytest의 caplog fixture 사용)"""
    with caplog.at_level(logging.INFO):
        response = client.get("/")
        
        assert response.status_code == 200
        
        # 로그 메시지 확인
        log_messages = [record.message for record in caplog.records]
        assert any("요청 시작" in msg for msg in log_messages)
        assert any("요청 완료" in msg for msg in log_messages)

def test_process_time_header():
    """처리 시간 헤더 테스트"""
    response = client.get("/")
    
    assert "X-Process-Time" in response.headers
    process_time = float(response.headers["X-Process-Time"])
    assert process_time > 0
```

---

## 3.7 환경 변수 관리

### 3.7.1 pydantic-settings 설치

```bash
pip install pydantic-settings
```

### 3.7.2 설정 파일 작성

**설정 모델** (`app/config.py`):
```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    """애플리케이션 설정"""
    
    # 앱 설정
    app_name: str = "Kaira Static Server"
    debug: bool = False
    environment: str = "development"
    
    # 서버 설정
    host: str = "0.0.0.0"
    port: int = 8000
    
    # 정적 파일 경로
    static_dir: str = "kaira-1.0.0"
    
    # 로그 설정
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # 데이터베이스 (향후 사용)
    database_url: str = "sqlite:///./app.db"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @property
    def static_path(self) -> Path:
        """정적 파일 절대 경로"""
        return Path(__file__).parent.parent / self.static_dir

# 전역 설정 인스턴스
settings = Settings()
```

### 3.7.3 .env 파일 작성

**개발 환경** (`.env`):
```bash
# .env
APP_NAME=Kaira Static Server
DEBUG=true
ENVIRONMENT=development

HOST=127.0.0.1
PORT=8000

STATIC_DIR=kaira-1.0.0

LOG_LEVEL=DEBUG
LOG_FILE=logs/app.log

DATABASE_URL=sqlite:///./dev.db
```

**운영 환경** (`.env.production`):
```bash
# .env.production
APP_NAME=Kaira Static Server
DEBUG=false
ENVIRONMENT=production

HOST=0.0.0.0
PORT=80

STATIC_DIR=/var/www/kaira-1.0.0

LOG_LEVEL=WARNING
LOG_FILE=/var/log/kaira/app.log

DATABASE_URL=postgresql://user:pass@localhost/kaira
```

### 3.7.4 설정 사용하기

**메인 앱에서 사용** (`app/main.py`):
```python
# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug
)

# 정적 파일 마운트 (경로가 존재하는 경우)
if settings.static_path.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(settings.static_path)),
        name="static"
    )

@app.get("/")
async def root():
    return {
        "app": settings.app_name,
        "environment": settings.environment
    }

@app.get("/config")
async def get_config():
    """현재 설정 확인 (개발 환경에서만)"""
    if not settings.debug:
        return {"error": "Not available in production"}
    
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "static_dir": str(settings.static_path),
        "log_level": settings.log_level
    }
```

### 3.7.5 테스트 환경 설정

```python
# tests/conftest.py
import pytest
import os
from app.config import Settings

@pytest.fixture(scope="session")
def test_settings():
    """테스트용 설정"""
    # 테스트 환경 변수 설정
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DEBUG"] = "true"
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"
    
    settings = Settings()
    yield settings
    
    # 정리
    del os.environ["ENVIRONMENT"]
    del os.environ["DEBUG"]
    del os.environ["DATABASE_URL"]

# tests/test_config.py
def test_settings(test_settings):
    """설정 테스트"""
    assert test_settings.environment == "testing"
    assert test_settings.debug is True
    assert "memory" in test_settings.database_url
```

### 3.7.6 중첩된 설정 관리

```python
# app/config.py 확장
from pydantic import BaseModel

class DatabaseSettings(BaseModel):
    """데이터베이스 설정"""
    url: str = "sqlite:///./app.db"
    echo: bool = False
    pool_size: int = 5

class LoggingSettings(BaseModel):
    """로깅 설정"""
    level: str = "INFO"
    file: str = "logs/app.log"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

class Settings(BaseSettings):
    """전체 설정"""
    app_name: str = "Kaira Static Server"
    debug: bool = False
    
    # 중첩 설정
    database: DatabaseSettings = DatabaseSettings()
    logging: LoggingSettings = LoggingSettings()
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__"  # DATABASE__URL 형식 지원
    )

settings = Settings()
```

**.env 파일 예시**:
```bash
# .env
APP_NAME=Kaira Static Server
DEBUG=true

# 데이터베이스 설정 (중첩)
DATABASE__URL=postgresql://user:pass@localhost/kaira
DATABASE__ECHO=true
DATABASE__POOL_SIZE=10

# 로깅 설정 (중첩)
LOGGING__LEVEL=DEBUG
LOGGING__FILE=logs/app.log
```

---

## 3.8 테스트 커버리지

### 3.8.1 pytest-cov 사용

**커버리지 측정**:
```bash
# 커버리지 리포트와 함께 테스트 실행
pytest --cov=app --cov-report=html --cov-report=term

# 누락된 줄 표시
pytest --cov=app --cov-report=term-missing
```

**출력 예시**:
```
---------- coverage: platform darwin, python 3.11.0 -----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
app/__init__.py              0      0   100%
app/main.py                 25      2    92%   45-46
app/config.py               30      0   100%
app/models.py               20      1    95%   34
------------------------------------------------------
TOTAL                       75      3    96%
```

### 3.8.2 HTML 리포트 생성

```bash
# HTML 리포트 생성
pytest --cov=app --cov-report=html

# 브라우저로 리포트 열기
open htmlcov/index.html  # macOS
```

**생성되는 파일**:
```
htmlcov/
├── index.html           # 메인 페이지
├── app_main_py.html     # app/main.py 상세 커버리지
├── app_config_py.html   # app/config.py 상세 커버리지
└── ... (기타 파일들)
```

### 3.8.3 커버리지 설정 파일

**`.coveragerc` 파일**:
```ini
# .coveragerc
[run]
source = app
omit = 
    */tests/*
    */venv/*
    */__pycache__/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:

[html]
directory = htmlcov
```

**사용**:
```bash
# .coveragerc 파일 사용
pytest --cov

# 또는 pyproject.toml에 설정 추가
```

### 3.8.4 최소 커버리지 설정

```bash
# 90% 미만이면 실패
pytest --cov=app --cov-fail-under=90
```

**CI/CD에서 활용**:
```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-fail-under=80
```

---

## 3.9 실전 예제

### 3.9.1 완전한 프로젝트 구조

```
kaira-server/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── logging_config.py
│   ├── models.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── logging.py
│   └── routers/
│       ├── __init__.py
│       └── items.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_config.py
│   ├── test_models.py
│   └── test_routers/
│       ├── __init__.py
│       └── test_items.py
├── logs/
│   └── app.log
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── pytest.ini
```

### 3.9.2 pytest.ini 설정

```ini
# pytest.ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 경고 설정
filterwarnings =
    error
    ignore::UserWarning
    ignore::DeprecationWarning

# 마커 정의
markers =
    slow: 느린 테스트 (선택적 실행)
    integration: 통합 테스트
    unit: 단위 테스트

# 출력 설정
addopts = 
    -v
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
```

### 3.9.3 conftest.py 완성

```python
# tests/conftest.py
import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.config import Settings

# ============== Fixtures ==============

@pytest.fixture(scope="session")
def test_settings():
    """테스트용 설정"""
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["DEBUG"] = "true"
    settings = Settings()
    yield settings
    del os.environ["ENVIRONMENT"]
    del os.environ["DEBUG"]

@pytest.fixture(scope="module")
def test_client():
    """TestClient 인스턴스"""
    with TestClient(app) as client:
        yield client

@pytest.fixture
def sample_item():
    """샘플 아이템 데이터"""
    return {
        "name": "테스트 상품",
        "price": 10000,
        "quantity": 5
    }

@pytest.fixture(autouse=True)
def reset_db():
    """각 테스트 전후로 DB 초기화 (자동 실행)"""
    # 테스트 전: 데이터 초기화
    yield
    # 테스트 후: 정리 작업

# ============== Pytest Hooks ==============

def pytest_configure(config):
    """pytest 설정 초기화"""
    config.addinivalue_line("markers", "slow: slow tests")

def pytest_collection_modifyitems(config, items):
    """테스트 수집 후 실행"""
    for item in items:
        # 통합 테스트 마커 자동 추가
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
```

### 3.9.4 완전한 테스트 예제

```python
# tests/test_complete.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# ============== 단위 테스트 ==============

@pytest.mark.unit
class TestUnit:
    """단위 테스트 모음"""
    
    def test_root_endpoint(self):
        """루트 엔드포인트 테스트"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_health_check(self):
        """헬스 체크 테스트"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

# ============== 통합 테스트 ==============

@pytest.mark.integration
class TestIntegration:
    """통합 테스트 모음"""
    
    def test_create_and_get_item(self):
        """아이템 생성 후 조회"""
        # 생성
        create_response = client.post(
            "/items/",
            json={"name": "책", "price": 15000}
        )
        assert create_response.status_code == 200
        item_id = create_response.json()["id"]
        
        # 조회
        get_response = client.get(f"/items/{item_id}")
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "책"

# ============== 매개변수화 테스트 ==============

@pytest.mark.parametrize("item_id,expected_status", [
    (1, 200),       # 존재하는 ID
    (999, 404),     # 존재하지 않는 ID
    ("abc", 422),   # 잘못된 형식
])
def test_get_item_status_codes(item_id, expected_status):
    """다양한 상태 코드 테스트"""
    response = client.get(f"/items/{item_id}")
    assert response.status_code == expected_status

# ============== Fixture 활용 ==============

@pytest.fixture
def created_item(test_client):
    """테스트용 아이템 생성"""
    response = test_client.post(
        "/items/",
        json={"name": "테스트 아이템", "price": 5000}
    )
    yield response.json()
    # 정리: 생성된 아이템 삭제 (필요시)

def test_with_fixture(created_item):
    """Fixture 사용 예제"""
    assert created_item["name"] == "테스트 아이템"
    assert created_item["price"] == 5000

# ============== 느린 테스트 ==============

@pytest.mark.slow
def test_slow_operation():
    """오래 걸리는 테스트 (선택적 실행)"""
    import time
    time.sleep(2)
    assert True
```

**선택적 테스트 실행**:
```bash
# 단위 테스트만 실행
pytest -m unit

# 통합 테스트 제외
pytest -m "not integration"

# 느린 테스트 제외
pytest -m "not slow"

# 특정 클래스만 실행
pytest tests/test_complete.py::TestUnit
```

---

## 3.10 문제 해결

### 3.10.1 자주 발생하는 문제

#### 문제 1: ModuleNotFoundError

**증상**:
```
ModuleNotFoundError: No module named 'app'
```

**해결**:
```bash
# pytest.ini에 pythonpath 설정
[pytest]
pythonpath = .

# 또는 환경 변수 설정
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

#### 문제 2: Fixture 순환 참조

**증상**:
```
fixture 'test_client' not found
```

**해결**:
```python
# tests/conftest.py에 fixture 정의
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as client:
        yield client
```

#### 문제 3: 비동기 함수 테스트

**증상**:
```
RuntimeWarning: coroutine was never awaited
```

**해결**:
```bash
# pytest-asyncio 설치
pip install pytest-asyncio
```

```python
# tests/test_async.py
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """비동기 함수 테스트"""
    result = await some_async_function()
    assert result is not None
```

### 3.10.2 디버깅 팁

```bash
# 상세 출력
pytest -vv

# 표준 출력 표시
pytest -s

# 첫 번째 실패에서 중단
pytest -x

# 실패한 테스트만 재실행
pytest --lf

# 특정 테스트 디버깅
pytest tests/test_main.py::test_root -vv -s

# PDB 디버거 사용
pytest --pdb
```

### 3.10.3 성능 문제

**느린 테스트 찾기**:
```bash
# 가장 느린 테스트 10개 표시
pytest --durations=10

# 모든 테스트의 실행 시간 표시
pytest --durations=0
```

**병렬 실행** (pytest-xdist):
```bash
# 설치
pip install pytest-xdist

# 4개의 워커로 병렬 실행
pytest -n 4

# CPU 코어 수만큼 자동 설정
pytest -n auto
```

---

## 3.11 체크리스트

프로젝트에 다음 항목들이 구현되었는지 확인하세요:

### 테스트 작성

- [ ] `tests/` 디렉토리 생성
- [ ] `tests/conftest.py` 작성 (공통 fixture)
- [ ] API 엔드포인트 테스트 작성
- [ ] 모델 검증 테스트 작성
- [ ] 에러 처리 테스트 작성
- [ ] 커버리지 90% 이상 달성

### Pytest 활용

- [ ] `pytest.ini` 설정 파일 작성
- [ ] Fixture로 재사용 가능한 테스트 데이터 정의
- [ ] Parametrize로 다양한 입력값 테스트
- [ ] 테스트 마커 활용 (unit, integration, slow)
- [ ] 테스트 실행 자동화 스크립트

### 에러 처리

- [ ] HTTPException 적절히 사용
- [ ] 커스텀 예외 클래스 정의
- [ ] 예외 핸들러 등록
- [ ] 검증 에러 커스터마이징
- [ ] 에러 응답 형식 통일

### 로깅

- [ ] 로깅 설정 모듈 작성 (`logging_config.py`)
- [ ] 로그 레벨 환경별 분리 (DEBUG, INFO, WARNING)
- [ ] 파일 로그와 콘솔 로그 설정
- [ ] 미들웨어로 요청/응답 로깅
- [ ] 로그 로테이션 설정 (선택사항)

### 환경 변수

- [ ] `pydantic-settings` 설치
- [ ] `app/config.py` 작성
- [ ] `.env` 파일 작성
- [ ] `.env.example` 템플릿 제공
- [ ] `.gitignore`에 `.env` 추가
- [ ] 환경별 설정 분리 (dev, staging, prod)

### 커버리지

- [ ] `pytest-cov` 설치
- [ ] `.coveragerc` 설정 파일 작성
- [ ] HTML 커버리지 리포트 생성
- [ ] CI/CD에 커버리지 체크 추가
- [ ] 최소 커버리지 기준 설정

### 문서화

- [ ] 각 테스트 함수에 docstring 추가
- [ ] README에 테스트 실행 방법 설명
- [ ] API 에러 코드 문서화
- [ ] 로깅 정책 문서화

---

## 📚 다음 단계

3단계를 완료했다면, 이제 다음을 진행할 수 있습니다:

1. **4단계: Docker 컨테이너화** (`04_DOCKER_GUIDE.md`)
   - Dockerfile 작성
   - docker-compose 활용
   - 컨테이너 최적화

2. **2단계 복습**: Poetry 환경에서 테스트 실행
   ```bash
   poetry add --group dev pytest pytest-cov pytest-asyncio
   poetry run pytest
   ```

3. **코드 품질 도구 추가**:
   ```bash
   # Linter와 Formatter 설치
   pip install black flake8 mypy
   
   # 실행
   black app/ tests/
   flake8 app/ tests/
   mypy app/
   ```

---

## 🎯 핵심 요약

이번 단계에서 배운 내용:

1. **Pytest**: Python 테스트 프레임워크의 표준
2. **TestClient**: FastAPI 테스트를 위한 도구
3. **HTTPException**: 표준화된 에러 처리
4. **Logging**: 체계적인 로그 관리
5. **pydantic-settings**: 타입 안전한 환경 변수 관리
6. **Coverage**: 테스트 품질 측정

**핵심 명령어**:
```bash
# 테스트 실행
pytest

# 커버리지와 함께 실행
pytest --cov=app --cov-report=html

# 특정 마커만 실행
pytest -m unit

# 병렬 실행
pytest -n auto
```

이제 테스트와 로깅이 완비된 견고한 FastAPI 애플리케이션을 만들 수 있습니다! 🎉

---

**작성일**: 2025-01-XX  
**최종 검증**: FastAPI 0.115.x, pytest 7.4+, pydantic-settings 2.x
