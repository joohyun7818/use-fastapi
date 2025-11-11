# 07. FastAPI 실전 프로젝트 구조 (Layered Architecture)

FastAPI 튜토리얼과 간단한 예제들은 대부분 단일 파일(`main.py`)에 모든 코드를 작성합니다. 이는 프레임워크의 기능을 빠르게 학습하는 데는 유용하지만, 실제 서비스를 개발하고 운영하기에는 적합하지 않은 구조입니다.

애플리케이션의 규모가 커지고 기능이 복잡해질수록, 유지보수성, 확장성, 그리고 팀원 간의 협업 효율성을 위해 체계적인 구조 설계가 필수적입니다.

이번 가이드에서는 Spring 프레임워크의 아키텍처와 유사한 **계층형 아키텍처(Layered Architecture)**를 FastAPI 프로젝트에 적용하고, **의존성 주입(Dependency Injection)**을 통해 각 계층을 효과적으로 연결하는 최신 방법을 소개합니다.

## 1. 왜 계층형 아키텍처가 필요한가?

계층형 아키텍처는 소프트웨어의 각 부분을 역할에 따라 논리적인 계층으로 분리하는 설계 패턴입니다. 핵심적인 장점은 다음과 같습니다.

-   **관심사 분리 (Separation of Concerns)**: 각 계층은 자신만의 명확한 책임과 역할을 가집니다. 이로 인해 코드의 이해가 쉬워지고, 특정 기능의 수정이 다른 부분에 미치는 영향을 최소화할 수 있습니다.
-   **유지보수 및 확장 용이성**: 기능 추가나 변경 시, 관련된 계층의 코드만 수정하면 되므로 생산성이 향상됩니다. 예를 들어, 데이터베이스를 PostgreSQL에서 MySQL로 변경할 때 데이터 접근 계층만 수정하면 됩니다.
-   **테스트 용이성**: 각 계층을 독립적으로 테스트하기 수월해집니다. 데이터베이스 연결 없이도 비즈니스 로직을 검증하는 단위 테스트 작성이 가능해집니다.
-   **협업 효율성**: 프론트엔드 개발자는 API 명세만 알면 되고, 백엔드 개발자는 각자 맡은 계층(API, 비즈니스 로직, 데이터베이스)에 집중하여 개발을 진행할 수 있습니다.

## 2. FastAPI 표준 프로젝트 폴더 구조

Spring Boot가 `controller`, `service`, `repository` 등으로 패키지를 나누는 것처럼, FastAPI 프로젝트도 역할에 따라 디렉토리를 명확하게 분리하는 것이 좋습니다.

### 2.1. 추천 폴더 구조 (현재 프로젝트 적용 구조)

```
kaira-fastapi-poetry/
├── pyproject.toml              # Poetry 의존성 및 설정
├── .env                        # 환경변수 (DATABASE_URL, DEBUG)
├── src/
│   └── kaira_fastapi_poetry/
│       ├── __init__.py
│       ├── main.py             # FastAPI 앱 생성 및 라우터 등록 (최상위 진입점)
│       │
│       ├── database.py         # 데이터베이스 연결 설정 (DeclarativeBase, 세션 관리)
│       │
│       ├── models.py           # SQLAlchemy ORM 모델 (User, Post)
│       │
│       ├── schemas.py          # Pydantic 스키마 (요청/응답 데이터 형식)
│       │
│       ├── crud.py             # CRUD 함수 (Create, Read, Update, Delete)
│       │
│       ├── config.py           # 앱 설정 (로깅, API 버전 등)
│       │
│       ├── logging_config.py   # 로깅 설정 (로그 파일, 레벨 등)
│       │
│       ├── api/                # 프레젠테이션 계층 (API 엔드포인트)
│       │   ├── __init__.py
│       │   ├── users.py        # 사용자 관련 엔드포인트 (POST, GET, PUT, DELETE)
│       │   └── posts.py        # 게시물 관련 엔드포인트 (POST, GET, PUT, DELETE)
│       │
│       ├── middleware/         # 미들웨어 (요청/응답 전처리)
│       │   ├── __init__.py
│       │   └── logging.py      # 요청/응답 로깅
│       │
│       ├── utils/              # 공통 유틸리티 함수
│       │   ├── __init__.py
│       │   └── helpers.py
│       │
│       └── kaira-1.0.0/        # 정적 파일 (HTML, CSS, JS)
│           ├── index.html
│           ├── css/
│           └── js/
│
├── tests/                      # 테스트 코드
│   ├── __init__.py
│   ├── test_main.py           # 메인 앱 테스트
│   └── ...
│
└── logs/                       # 애플리케이션 로그 파일
```

### 2.2. Spring Boot 구조와 비교

| FastAPI 구조 | Spring Boot 구조 | 역할 (책임) | 계층 |
| :--- | :--- | :--- | :--- |
| `api/users.py`, `api/posts.py` | `controller/` | HTTP 요청 처리, 데이터 유효성 검사, 서비스 호출 | **프레젠테이션** |
| `schemas.py` | `dto/` | API 요청/응답 데이터 형태 정의 (DTO) | **프레젠테이션** |
| `crud.py` | `service/` | 비즈니스 로직 및 데이터 조작 | **비즈니스/데이터 접근** |
| `models.py` | `entity/` | 데이터베이스 테이블과 매핑되는 ORM 모델 | **데이터 접근** |
| `database.py` | `config/` | DB 연결, 세션 관리 | **인프라** |
| `config.py`, `logging_config.py` | `config/` | 앱 설정 및 환경 관리 | **인프라** |


## 3. 실전 구조 - kaira-fastapi-poetry 프로젝트

현재 진행 중인 `kaira-fastapi-poetry` 프로젝트는 위의 권장 구조를 실제로 구현한 사례입니다. 각 파일의 역할을 살펴보겠습니다.

### 3.1 데이터베이스 계층 - `database.py`

데이터베이스 연결 및 세션 관리:

```python
# src/kaira_fastapi_poetry/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# 환경변수에서 DATABASE_URL 읽기
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    """FastAPI 의존성 주입용 세션 제공"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 3.2 모델 계층 - `models.py`

SQLAlchemy ORM 모델:

```python
# src/kaira_fastapi_poetry/models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 정의: 한 사용자는 여러 게시물을 가질 수 있음
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("user.id"))
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 관계 정의: 게시물은 한 사용자에게만 속함
    author = relationship("User", back_populates="posts")
```

### 3.3 스키마 계층 - `schemas.py`

Pydantic 데이터 검증 및 변환:

```python
# src/kaira_fastapi_poetry/schemas.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
```

### 3.4 CRUD 계층 - `crud.py`

데이터베이스 작업 함수:

```python
# src/kaira_fastapi_poetry/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# ===== User CRUD =====
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hash_password = user.password + "notreallyhashed"
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=fake_hash_password,
        full_name=user.full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# ===== Post CRUD =====
def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_published_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Post).filter(
        models.Post.is_published == True
    ).offset(skip).limit(limit).all()

def get_posts_by_author(db: Session, author_id: int):
    return db.query(models.Post).filter(
        models.Post.author_id == author_id
    ).all()

def create_post(db: Session, post: schemas.PostCreate, author_id: int):
    db_post = models.Post(
        title=post.title,
        content=post.content,
        author_id=author_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate):
    db_post = get_post(db, post_id)
    if not db_post:
        return None
    
    update_data = post_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int):
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
```

### 3.5 프레젠테이션 계층 - `api/users.py`

사용자 엔드포인트:

```python
# src/kaira_fastapi_poetry/api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=list[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db)
):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", response_model=schemas.UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

### 3.6 프레젠테이션 계층 - `api/posts.py`

게시물 엔드포인트:

```python
# src/kaira_fastapi_poetry/api/posts.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: schemas.PostCreate,
    author_id: int,
    db: Session = Depends(get_db)
):
    # 작성자가 존재하는지 확인
    author = crud.get_user(db, user_id=author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_post(db=db, post=post, author_id=author_id)

@router.get("/", response_model=list[schemas.PostResponse])
def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/published", response_model=list[schemas.PostResponse])
def list_published_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_published_posts(db, skip=skip, limit=limit)
    return posts

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.put("/{post_id}", response_model=schemas.PostResponse)
def update_post(
    post_id: int,
    post_update: schemas.PostUpdate,
    db: Session = Depends(get_db)
):
    db_post = crud.update_post(db, post_id=post_id, post_update=post_update)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.delete("/{post_id}", response_model=schemas.PostResponse)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.delete_post(db, post_id=post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
```

### 3.7 메인 애플리케이션 - `main.py`

앱 초기화 및 라우터 등록:

```python
# src/kaira_fastapi_poetry/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import logging
from .api import users, posts
from .database import engine, Base
from .logging_config import setup_logging
from .config import settings
import os

# 로깅 설정
setup_logging()
logger = logging.getLogger(__name__)

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Kaira FastAPI Server",
    description="Modern FastAPI with SQLAlchemy and Pydantic",
    version=settings.API_VERSION
)

# 정적 파일 마운트
static_dir = os.path.join(os.path.dirname(__file__), "kaira-1.0.0")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 라우터 등록
app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Kaira FastAPI Server"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "kaira-server"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "kaira_fastapi_poetry.main:app",
        host="127.0.0.1",
        port=9000,
        reload=True
    )
```

---

## 3.8 계층형 아키텍처의 흐름도

```
HTTP 요청
    ↓
[API Layer] (api/users.py, api/posts.py)
    ↓ (유효성 검사, 요청 매핑)
[CRUD Layer] (crud.py)
    ↓ (비즈니스 로직)
[Database Layer] (models.py, database.py)
    ↓ (DB 쿼리 실행)
[PostgreSQL Database]
    ↓
[Response] (schemas.py)
    ↓
HTTP 응답
```

---



### 단계 0: 모든 로직이 포함된 `main.py`

```python
# main.py (리팩토링 전)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

# 임시 데이터베이스 (메모리)
fake_db: Dict[int, Dict] = {}
user_counter = 0

# DTO 역할의 Pydantic 모델
class UserCreate(BaseModel):
    username: str
    email: str

class User(BaseModel):
    id: int
    username: str
    email: str

@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    global user_counter
    # 이메일 중복 체크 (비즈니스 로직)
    for db_user in fake_db.values():
        if db_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # 새 사용자 ID 생성 및 저장 (데이터 접근 로직)
    user_counter += 1
    new_user = {"id": user_counter, "username": user.username, "email": user.email}
    fake_db[user_counter] = new_user
    
    return new_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    # 사용자 조회 (데이터 접근 로직)
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]
```
위 코드는 비즈니스 로직과 데이터 접근 로직이 API 엔드포인트에 뒤섞여 있어 유지보수가 어렵습니다.

### 단계 1: `schemas` 와 `models` 분리

먼저 데이터의 형태를 정의하는 부분을 분리합니다.

-   `app/models/user.py`: 데이터베이스 테이블과 직접 매핑되는 모델입니다. (ORM 사용 시)
```python
# 여기서는 간단한 Dict로 대체하지만, SQLAlchemy 사용 시 ORM 모델이 위치합니다.
from typing import TypedDict

class User(TypedDict):
    id: int
    username: str
    email: str
```

-   `app/api/schemas.py`: API의 요청/응답 데이터 형식을 정의합니다.
```python
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }
```

### 단계 2: `repository` 계층 분리 (Data Access)

데이터베이스와의 통신을 담당하는 `repository`를 만듭니다. 실제 프로젝트에서는 `database.py`에서 생성한 DB 세션(`db: Session`)을 주입받아 사용합니다.

-   `app/repository/user_repository.py`:
```python
from typing import Dict, Optional
from ..models.user import User

# 임시 데이터베이스 (실제로는 DB 세션이 이 역할을 대체)
_fake_db: Dict[int, User] = {}
_user_counter = 0

class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[User]:
        return _fake_db.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        for user in _fake_db.values():
            if user["email"] == email:
                return user
        return None

    def create(self, username: str, email: str) -> User:
        global _user_counter
        _user_counter += 1
        new_user = User(id=_user_counter, username=username, email=email)
        _fake_db[_user_counter] = new_user
        return new_user
```

### 단계 3: `service` 계층 분리 (Business Logic)

비즈니스 로직을 처리하는 `service`를 만듭니다. `service`는 `repository`에 의존합니다.

-   `app/services/user_service.py`:
```python
from fastapi import HTTPException
from ..repository.user_repository import UserRepository
from ..api.schemas import UserCreate

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def create_user(self, user_data: UserCreate):
        # 이메일 중복 체크 (비즈니스 로직)
        if self.user_repo.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 사용자 생성 요청
        return self.user_repo.create(username=user_data.username, email=user_data.email)

    def get_user(self, user_id: int):
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
```

### 단계 4: `api` 계층과 의존성 주입 설정

이제 각 계층을 FastAPI의 의존성 주입 시스템으로 연결합니다. `api/deps.py` 파일에서 의존성을 정의하고, `routers`에서 이를 사용합니다.

-   `app/api/deps.py`:
```python
from ..repository.user_repository import UserRepository
from ..services.user_service import UserService

# Repository 인스턴스는 요청마다 새로 생성할 수도 있고, 싱글톤으로 유지할 수도 있습니다.
# 여기서는 간단하게 싱글톤 인스턴스를 생성합니다.
user_repository = UserRepository()

def get_user_service() -> UserService:
    return UserService(user_repository)
```

-   `app/api/routers/users.py` (최종):
```python
from fastapi import APIRouter, Depends, HTTPException
from ..schemas import UserSchema, UserCreate
from ..services.user_service import UserService
from .deps import get_user_service

router = APIRouter()

@router.post("/", response_model=UserSchema)
def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    # 비즈니스 로직은 서비스 계층에 완전히 위임
    # 서비스 계층에서 발생하는 HTTPException을 그대로 사용
    return user_service.create_user(user_data)

@router.get("/{user_id}", response_model=UserSchema)
def read_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service)
):
    # 비즈니스 로직은 서비스 계층에 완전히 위임
    return user_service.get_user(user_id)
```

-   `app/main.py`:
```python
from fastapi import FastAPI
from .api.routers import users

app = FastAPI(title="My FastAPI Project")

app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the main page"}
```

이제 각 파일은 자신의 역할에만 집중합니다.
-   `users.py`는 HTTP 요청과 응답, 그리고 의존성 주입에만 집중합니다.
-   `user_service.py`는 이메일 중복 확인과 같은 비즈니스 규칙에만 집중합니다.
-   `user_repository.py`는 데이터 저장 및 조회 방법에만 집중합니다.

## 4. 의존성 주입의 장점

FastAPI의 `Depends`를 사용한 의존성 주입은 다음과 같은 강력한 이점을 제공합니다.

1.  **명시적인 의존성**: 코드만 봐도 어떤 컴포넌트가 다른 컴포넌트를 필요로 하는지 명확하게 알 수 있습니다.
2.  **쉬운 테스트**: 테스트 시 실제 `repository`나 `service` 대신 가짜(mock) 객체를 쉽게 주입할 수 있습니다. 이를 통해 외부 시스템(DB 등)에 대한 의존성 없이 순수한 비즈니스 로직을 테스트할 수 있습니다.
3.  **재사용성**: `deps.py`에 정의된 의존성은 여러 라우터에서 재사용될 수 있습니다. 예를 들어, `get_current_user`와 같은 인증 의존성을 만들어 여러 엔드포인트에 적용할 수 있습니다.

## 결론

FastAPI는 특정 구조를 강제하지 않는 유연한 프레임워크이지만, 프로젝트의 지속 가능성을 위해서는 처음부터 체계적인 구조를 잡는 것이 매우 중요합니다. Spring 개발 경험이 있다면, 위에서 소개한 계층형 아키텍처와 의존성 주입 패턴을 FastAPI에 적용하는 것이 자연스럽고 효과적인 방법이 될 것입니다.

이 구조를 기본 틀로 삼아 프로젝트를 시작하면, 향후 기능 추가 및 유지보수가 훨씬 수월해질 것입니다.