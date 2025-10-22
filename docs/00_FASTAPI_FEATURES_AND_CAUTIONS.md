# 0장: FastAPI의 특징과 주의점

## 📖 이 장의 목적

FastAPI는 현대적인 Python 웹 프레임워크로, 높은 성능과 개발자 경험을 제공합니다. 이 장에서는 FastAPI의 핵심 특징과 개발 시 주의해야 할 중요한 점들을 살펴보겠습니다.

---

## 🚀 FastAPI의 주요 특징

### 1. **고성능 비동기 프레임워크**

FastAPI는 **Starlette**와 **Pydantic**을 기반으로 하는 최신 Python 웹 프레임워크입니다.

**주요 특징:**
- **비동기 지원**: asyncio 기반으로 동시성 처리에 강력
- **타입 힌트 활용**: Python 타입 힌트를 최대한 활용한 API 설계
- **자동 문서화**: OpenAPI/Swagger 기반 자동 API 문서 생성
- **고성능**: NodeJS, Go와 유사한 수준의 성능

**성능 비교 (요청/초):**
- FastAPI: ~25,000
- Flask: ~5,000
- Django: ~3,000

### 2. **개발자 경험 (DX) 중심 설계**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return item
```

**DX 장점:**
- **자동 검증**: 요청/응답 데이터 자동 검증
- **타입 안전성**: IDE 지원으로 실시간 에러 감지
- **자동 완성**: 코드 작성 시 자동 완성 지원
- **실시간 문서**: 코드 변경 시 문서 자동 업데이트

### 3. **Pydantic 기반 데이터 검증**

```python
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=50)
    email: Optional[str] = None
    age: int = Field(..., ge=0, le=150)
```

**Pydantic의 강점:**
- **자동 타입 변환**: JSON ↔ Python 객체 자동 변환
- **강력한 검증**: 정규식, 범위, 커스텀 검증 지원
- **에러 메시지**: 상세한 검증 에러 제공
- **직렬화**: dict/JSON 자동 변환

### 4. **의존성 주입 시스템**

```python
from fastapi import Depends

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await auth_service.verify_token(token)

@app.get("/users/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
```

**의존성 주입의 장점:**
- **코드 재사용**: 인증, DB 연결 등 공통 로직 재사용
- **테스트 용이성**: 의존성 모킹으로 단위 테스트 용이
- **유연성**: 런타임에 의존성 교체 가능

---

## ⚠️ FastAPI 개발 시 주의사항

### 1. **Async/Await 규칙**

#### ✅ 올바른 사용
```python
# FastAPI에서는 항상 async def 사용
@app.get("/items")
async def get_items():  # async def 필수
    return await database.fetch_items()  # I/O 시 await

@app.get("/health")
async def health_check():  # async def 필수 (동기 작업만 해도)
    return {"status": "ok"}  # await 불필요
```

#### ❌ 잘못된 사용
```python
# 동기 함수에서 await 사용
def sync_function():
    result = await database.query()  # ❌ SyntaxError

# FastAPI에서 동기 함수 사용
@app.get("/items")
def get_items():  # ❌ FastAPI가 인식하지 못함
    return database.fetch_items()
```

**핵심 규칙:**
- **FastAPI 함수**: 항상 `async def` 사용 (프레임워크 규칙)
- **await**: I/O 작업 시에만 사용 (선택적)

### 2. **타입 힌트 필수**

#### ✅ 권장 패턴
```python
from typing import List, Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    tags: Optional[List[str]] = None

@app.get("/items", response_model=List[Item])
async def get_items() -> List[Item]:
    return await database.get_items()
```

#### ❌ 타입 힌트 누락
```python
@app.get("/items")
async def get_items():  # 반환 타입 없음
    return await database.get_items()  # 문서화 부족
```

**타입 힌트의 이점:**
- **자동 문서화**: OpenAPI 스키마 자동 생성
- **IDE 지원**: 실시간 에러 감지 및 자동 완성
- **런타임 검증**: 요청/응답 데이터 검증

### 3. **Pydantic 모델 설계**

#### ✅ 모델 분리 원칙
```python
class ItemCreate(BaseModel):
    name: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    created_at: datetime

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    return await database.create_item(item)

@app.patch("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: ItemUpdate):
    return await database.update_item(item_id, item)
```

#### ❌ 한 모델로 모든 용도
```python
class Item(BaseModel):
    id: Optional[int] = None  # 생성 시 None, 응답 시 값 있음
    name: str
    password: str  # 응답에 비밀번호 노출!
    created_at: Optional[datetime] = None
```

### 4. **에러 처리**

#### ✅ HTTPException 사용
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await database.get_item(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item {item_id} not found"
        )
    return item
```

#### ✅ 커스텀 예외 핸들러
```python
from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "details": exc.errors()
        }
    )
```

### 5. **보안 고려사항**

#### ✅ 입력 검증 강화
```python
from pydantic import Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=8)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    # password 필드 제외 (보안)
```

#### ✅ CORS 설정
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 허용 도메인 제한
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 6. **성능 최적화**

#### ✅ 비동기 I/O 활용
```python
# ❌ 동기 I/O (블로킹)
import requests

@app.get("/external-data")
async def get_external_data():
    response = requests.get("https://api.example.com/data")  # 블로킹!
    return response.json()

# ✅ 비동기 I/O
import httpx

@app.get("/external-data")
async def get_external_data():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

#### ✅ 데이터베이스 연결 풀
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작: 연결 풀 생성
    app.state.db_pool = await create_database_pool()
    yield
    # 종료: 연결 풀 정리
    await app.state.db_pool.close()
```

### 7. **테스트 작성**

#### ✅ TestClient 활용
```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_item():
    response = client.post("/items", json={"name": "Test", "price": 100})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test"
    assert data["price"] == 100
```

#### ✅ 비동기 테스트
```python
import pytest

@pytest.mark.asyncio
async def test_database_operation():
    # 데이터베이스 테스트
    item = await database.create_item({"name": "Test"})
    assert item.name == "Test"
```

---

## 🎯 FastAPI 개발 모범 사례

### 1. **프로젝트 구조**
```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI 앱 인스턴스
│   ├── config.py        # 설정 관리
│   ├── models.py        # Pydantic 모델
│   ├── database.py      # DB 연결
│   ├── routers/         # API 라우터
│   ├── dependencies.py  # 의존성 함수
│   └── middleware.py    # 미들웨어
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # 테스트 설정
│   └── test_*.py        # 테스트 파일
├── requirements.txt
└── README.md
```

### 2. **환경별 설정**
```python
# config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    debug: bool = False
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. **API 버전 관리**
```python
app = FastAPI(
    title="My API",
    version="1.0.0",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

# 또는 URL에 버전 포함
@app.get("/api/v1/users")
async def get_users_v1():
    pass
```

---

## 🚨 자주 하는 실수들

### 1. **동기 함수에서 await 사용**
```python
def sync_function():
    result = await database.query()  # ❌ SyntaxError
```

### 2. **Pydantic 모델 오용**
```python
class User(BaseModel):
    password: str  # 응답에 비밀번호 노출! ❌
```

### 3. **무거운 작업을 동기로 처리**
```python
@app.get("/heavy")
async def heavy_task():
    time.sleep(10)  # 동기 sleep! ❌ 블로킹 발생
    return {"result": "done"}
```

### 4. **예외 처리 누락**
```python
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return await db.get_user(user_id)  # 에러 시 500 반환 ❌
```

### 5. **CORS 설정 누락**
```python
# 프론트엔드에서 API 호출 불가 ❌
app = FastAPI()  # CORS 미설정
```

---

## 📚 이 가이드의 구성

이 가이드는 FastAPI의 기초부터 고급 기능까지 단계적으로 학습할 수 있도록 구성되었습니다:

1. **0장: FastAPI의 특징과 주의점** (현재)
2. **1장: FastAPI CLI 활용 가이드**
3. **2장: Poetry 패키지 관리**
4. **3장: 테스트와 로깅**
5. **4장: Docker 컨테이너화**
6. **5장: 데이터베이스 연동**
7. **6장: 배포와 클라우드**

각 장에서는 실제 프로젝트를 통해 실습하며 FastAPI의 다양한 기능을 학습합니다.

---

## 🎯 핵심 요약

**FastAPI의 장점:**
- 고성능 비동기 프레임워크
- 뛰어난 개발자 경험
- 자동 타입 검증 및 문서화
- 강력한 의존성 주입 시스템

**주의해야 할 점:**
- 항상 `async def` 사용 (프레임워크 규칙)
- 타입 힌트 필수 활용
- Pydantic 모델 적절히 분리
- 보안 및 성능 고려
- 철저한 테스트 작성

FastAPI는 올바른 패턴을 따르면 매우 강력하고 유지보수하기 좋은 애플리케이션을 만들 수 있습니다. 이 가이드를 통해 FastAPI의 모든 기능을 마스터해보세요! 🚀

---

**작성일**: 2025년 10월 22일
**다음 장**: [1장: FastAPI CLI 활용 가이드](01_FASTAPI_CLI_GUIDE.md)