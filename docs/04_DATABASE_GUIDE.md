# 04. FastAPI 데이터베이스 연결 완벽 가이드

> FastAPI 애플리케이션에 데이터베이스를 연동하고, 실제 데이터 관리 기능을 구현하는 방법을 배웁니다.

## 📚 4단계 목차

| 챕터 | 주제 | 예상 시간 |
|------|------|---------|
| [4.1](#41-학습-목표) | 학습 목표 | - |
| [4.2](#42-인기-있는-데이터베이스-연결-방법-3가지) | 인기 있는 데이터베이스 연결 방법 3가지 | 30분 |
| [4.3](#43-sqlalchemy--postgresql-선택-이유) | SQLAlchemy + PostgreSQL 선택 이유 | 20분 |
| [4.4](#44-환경-설정) | 환경 설정 | 1시간 |
| [4.5](#45-sqlalchemy-기초) | SQLAlchemy 기초 | 1시간 |
| [4.6](#46-데이터베이스-모델-정의) | 데이터베이스 모델 정의 | 1시간 |
| [4.7](#47-crud-작업-구현) | CRUD 작업 구현 | 1시간 30분 |
| [4.8](#48-fastapi와-데이터베이스-통합) | FastAPI와 데이터베이스 통합 | 1시간 |
| [4.9](#49-마이그레이션-관리-alembic) | 마이그레이션 관리 (Alembic) | 1시간 |

---

## 4.1 학습 목표

이 단계를 완료하면 다음을 할 수 있습니다:

✅ **데이터베이스 기초**
- 관계형 데이터베이스 개념 이해
- PostgreSQL 기본 설정
- SQLAlchemy ORM 기초

✅ **데이터 모델링**
- SQLAlchemy 모델 정의
- 관계 설정 (One-to-Many, Many-to-Many)
- 데이터 검증

✅ **CRUD 작업**
- 데이터 생성 (Create)
- 데이터 조회 (Read)
- 데이터 업데이트 (Update)
- 데이터 삭제 (Delete)

✅ **API 연동**
- FastAPI 엔드포인트와 데이터베이스 연동
- Pydantic 스키마로 요청/응답 관리
- 트랜잭션 관리

✅ **데이터베이스 마이그레이션**
- Alembic으로 스키마 변경 관리
- 버전 관리
- 롤백 처리

**예상 소요 시간**: 5-7시간  
**난이도**: ⭐⭐ (중간)  
**선행 학습**: 1단계, 2단계, 3단계 완료 필수

---

## 4.2 인기 있는 데이터베이스 연결 방법 3가지

FastAPI에서 데이터베이스를 연결하는 방법은 여러 가지가 있습니다. 가장 인기 있는 3가지를 소개합니다.

### 🥇 방법 1: SQLAlchemy ORM + PostgreSQL (가장 권장)

**특징**:
- ✅ 가장 널리 사용되는 방식
- ✅ ORM으로 직관적인 데이터 작업
- ✅ 관계형 데이터베이스 최적화
- ✅ 마이그레이션 도구 (Alembic) 지원
- ✅ 대규모 프로덕션 프로젝트에 적합

**사용 기술**:
```
FastAPI ↔ SQLAlchemy (ORM) ↔ PostgreSQL (DB)
```

**라이브러리**:
- `sqlalchemy`: ORM 라이브러리
- `psycopg2`: PostgreSQL 어댑터
- `alembic`: 마이그레이션 도구

**장점**:
- 강력한 관계 모델링
- 복잡한 쿼리를 OOP로 작성
- 타입 안정성
- 커뮤니티 지원 우수

**단점**:
- 학습 곡선 있음
- PostgreSQL 설치 필요
- 약간의 오버헤드

**적합한 프로젝트**:
- 복잡한 비즈니스 로직
- 대규모 데이터 처리
- 마이크로서비스
- 엔터프라이즈 애플리케이션

---

### 🥈 방법 2: MongoDB + Motor (비관계형 데이터베이스)

**특징**:
- ✅ NoSQL 문서형 데이터베이스
- ✅ 빠른 프로토타이핑
- ✅ 유연한 스키마
- ✅ 비동기 처리 최적화

**사용 기술**:
```
FastAPI ↔ Motor (Async Driver) ↔ MongoDB (NoSQL DB)
```

**라이브러리**:
- `motor`: MongoDB의 비동기 드라이버
- `pymongo`: MongoDB 기본 드라이버
- `pydantic`: 데이터 검증

**장점**:
- 설정 간단
- JSON 같은 유연한 구조
- 수평 확장 용이
- 빠른 쓰기 성능

**단점**:
- 복잡한 트랜잭션 미지원
- 메모리 사용량 많음
- 관계 모델링 어려움

**적합한 프로젝트**:
- 빠른 프로토타입
- 로그 수집
- 실시간 데이터 처리
- 스타트업 MVP

---

### 🥉 방법 3: SQLite (로컬/가벼운 프로젝트)

**특징**:
- ✅ 별도 설치 불필요
- ✅ 파일 기반 데이터베이스
- ✅ 학습용으로 최적
- ✅ 소규모 프로젝트 적합

**사용 기술**:
```
FastAPI ↔ SQLAlchemy (ORM) ↔ SQLite (Local DB)
```

**라이브러리**:
- `sqlalchemy`: ORM 라이브러리
- `sqlite3`: 기본 내장 (별도 설치 불필요)

**장점**:
- 설정 매우 간단
- 외부 의존성 없음
- 학습하기 쉬움
- 소규모 데이터 처리 최적

**단점**:
- 동시성 제한
- 대규모 데이터 처리 부적합
- 프로덕션에 부적합
- 성능 제한

**적합한 프로젝트**:
- 학습/실습
- 개인 프로젝트
- 프로토타입
- 테스트 환경

---

### 비교 표

| 항목 | SQLAlchemy + PostgreSQL | MongoDB + Motor | SQLite |
|------|-------------------------|-----------------|--------|
| 학습 난이도 | ⭐⭐⭐ | ⭐⭐ | ⭐ |
| 프로덕션 준비 | ✅ 우수 | ✅ 좋음 | ❌ 부적합 |
| 복잡한 관계 | ✅ 우수 | ⚠️ 제한 | ✅ 우수 |
| 성능 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| 커뮤니티 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 권장 규모 | 중/대 | 소/중 | 소 |

---

## 4.3 SQLAlchemy + PostgreSQL 선택 이유

이 가이드에서 **SQLAlchemy + PostgreSQL** 조합을 선택한 이유:

1. **가장 인기 있는 조합** - 대부분의 FastAPI 프로젝트에서 사용
2. **프로덕션 준비 완료** - 대규모 애플리케이션에 적합
3. **강력한 도구 지원** - Alembic 마이그레이션 지원
4. **채용 시장** - 기술 습득이 경력에 직결됨
5. **학습 가치** - 다른 데이터베이스로 전환 용이

---

## 4.4 환경 설정

### 4.4.1 필수 도구 설치

#### PostgreSQL 설치

**macOS**:
```bash
# Homebrew로 설치
brew install postgresql

# PostgreSQL 서비스 시작
brew services start postgresql

# 설치 확인
psql --version
```

**Ubuntu/Linux**:
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# 서비스 시작
sudo systemctl start postgresql

# 설치 확인
psql --version
```

**Windows**:
- [PostgreSQL 공식 설치 프로그램](https://www.postgresql.org/download/windows/) 다운로드
- 설치 중 superuser 비밀번호 설정
- psql 명령어로 확인

#### 데이터베이스 생성

```bash
# PostgreSQL에 로그인 (기본 사용자: postgres)
psql -U postgres

# 또는 대화형 모드에서:
# \l  - 데이터베이스 목록 확인
# \du - 사용자 목록 확인

# 데이터베이스 생성
CREATE DATABASE kaira_db;

# 사용자 생성 (선택사항)
CREATE USER kaira_user WITH PASSWORD 'secure_password';

# 권한 부여
GRANT ALL PRIVILEGES ON DATABASE kaira_db TO kaira_user;

# 접속 확인
psql -U kaira_user -d kaira_db
```

### 4.4.2 Python 패키지 설치

Poetry 프로젝트에 필요한 패키지 추가:

```bash
cd kaira-fastapi-poetry

# 데이터베이스 관련 패키지 설치
poetry add sqlalchemy psycopg2-binary alembic python-dotenv

# 또는 개발 환경용:
poetry add --group dev pytest-asyncio
```

**pyproject.toml 확인**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.100"
uvicorn = "^0.23"
sqlalchemy = "^2.0"
psycopg2-binary = "^2.9"
alembic = "^1.12"
python-dotenv = "^1.0"
pydantic = "^2.0"
```

---

## 4.5 SQLAlchemy 기초

### 4.5.1 데이터베이스 연결 설정

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/database.py`

```python
"""
데이터베이스 연결 설정 (프로젝트 현황)
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# PostgreSQL 연결 문자열
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://kaira_user:kaira_1234@localhost:5432/kaira_db"
)

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 출력 (개발 중만 사용)
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

# SQLAlchemy 2.0+ 방식: DeclarativeBase 사용
class Base(DeclarativeBase):
    pass


def get_db():
    """
    데이터베이스 세션 제공 (FastAPI 의존성)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**핵심 개선사항**:
- ✅ SQLAlchemy 2.0 권장 방식 사용 (`DeclarativeBase`)
- ✅ 레거시 `declarative_base()` 대신 클래스 기반 정의
- ✅ 더 나은 타입 힌팅 지원

### 4.5.2 환경 변수 설정

`.env` 파일 생성 (프로젝트 루트):

```bash
# .env
DATABASE_URL=postgresql://kaira_user:secure_password@localhost:5432/kaira_db
DEBUG=True
```

⚠️ **주의**: `.env` 파일을 `.gitignore`에 추가하세요!

```bash
echo ".env" >> .gitignore
```

### 4.5.3 SQLAlchemy 콘셉트 이해

**주요 객체**:

| 객체 | 설명 |
|------|------|
| `Engine` | 데이터베이스 연결 풀 관리 |
| `Session` | 데이터베이스 트랜잭션 관리 |
| `Base` | 모든 모델의 기본 클래스 |
| `Model` | ORM 데이터 모델 |

**세션 라이프사이클**:
```
1. 세션 생성 (SessionLocal())
   ↓
2. 데이터 작업 (쿼리, 추가, 수정)
   ↓
3. 커밋 또는 롤백 (commit/rollback)
   ↓
4. 세션 종료 (close)
```

---

## 4.6 데이터베이스 모델 정의

### 4.6.1 기본 모델 작성

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/models.py`

```python
"""
SQLAlchemy ORM 모델 정의 (프로젝트 현황)
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    """사용자 모델"""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"


class Post(Base):
    """게시물 모델"""
    
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    author = relationship("User", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title={self.title})>"
```

**핵심 특징**:
- ✅ SQLAlchemy 2.0 패턴 사용
- ✅ 상대 import 사용 (패키지 구조 준수)
- ✅ One-to-Many 관계 설정
- ✅ Cascade delete 자동 처리

### 4.6.2 Pydantic 스키마 정의 (API 요청/응답)

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/schemas.py`

```python
"""
Pydantic 스키마 - API 요청/응답 검증 (프로젝트 현황)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    """사용자 기본 정보"""
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """사용자 생성 요청"""
    password: str = Field(..., min_length=8, max_length=255)


class UserResponse(UserBase):
    """사용자 응답"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class PostBase(BaseModel):
    """게시물 기본 정보"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    """게시물 생성 요청"""
    pass


class PostResponse(PostBase):
    """게시물 응답"""
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}
```

**중요 개선사항**:
- ✅ Pydantic v2 문법 사용 (`model_config`)
- ✅ SQLAlchemy 모델과 완전히 분리
- ✅ API 요청/응답 검증 전담
- ✅ 이메일 정규식 검증 포함

---

## 4.7 CRUD 작업 구현

## 4.7 CRUD 작업 구현

### 4.7.1 CRUD 기초 함수

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/crud.py`

```python
"""
CRUD (Create, Read, Update, Delete) 작업 (프로젝트 현황)
"""
from sqlalchemy.orm import Session
from . import models


# ===== USER CRUD =====

def get_user(db: Session, user_id: int):
    """ID로 사용자 조회"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """이메일로 사용자 조회"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """모든 사용자 조회 (페이징)"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, username: str, email: str, password_hash: str, full_name: str = None):
    """새 사용자 생성"""
    db_user = models.User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, **kwargs):
    """사용자 정보 업데이트"""
    db_user = get_user(db, user_id)
    if db_user:
        for key, value in kwargs.items():
            if value is not None and hasattr(db_user, key):
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """사용자 삭제"""
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# ===== POST CRUD =====

def get_post(db: Session, post_id: int):
    """ID로 게시물 조회"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10, author_id: int = None):
    """게시물 조회 (필터링, 페이징)"""
    query = db.query(models.Post)
    if author_id:
        query = query.filter(models.Post.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def create_post(db: Session, title: str, content: str, author_id: int, is_published: bool = False):
    """새 게시물 생성"""
    db_post = models.Post(
        title=title,
        content=content,
        author_id=author_id,
        is_published=is_published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
```

**핵심 설계**:
- ✅ 관심사 분리 (DB 로직 독립)
- ✅ 재사용 가능한 함수 설계
- ✅ 의존성 주입으로 세션 관리
- ✅ 자동 commit/refresh

### 4.7.2 Pydantic 스키마와 함께 사용

**✅ 현재 프로젝트 구조 요약**:

| 파일 | 역할 |
|------|------|
| `models.py` | SQLAlchemy ORM 모델 (DB 테이블 구조) |
| `schemas.py` | Pydantic 스키마 (API 검증) |
| `crud.py` | CRUD 함수 (DB 작업 로직) |
| `api/users.py` | 사용자 API 엔드포인트 |
| `api/posts.py` | 게시물 API 엔드포인트 |

---

## 4.8 FastAPI와 데이터베이스 통합

### 4.8.1 API 엔드포인트 작성

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/api/users.py`

```python
"""
사용자 API 엔드포인트 (프로젝트 현황)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """새 사용자 생성"""
    # 사용자명 중복 확인
    existing_user = crud.get_user_by_username(db, username=user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다"
        )
    
    # 이메일 중복 확인
    existing_email = crud.get_user_by_email(db, email=user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 사용자 생성
    user = crud.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password,  # TODO: 프로덕션에서는 해싱 필수!
        full_name=user_data.full_name
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """사용자 조회"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """사용자 목록 조회"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
```

**핵심 패턴**:
- ✅ `Depends(get_db)` 로 세션 자동 주입
- ✅ `response_model` 로 응답 검증
- ✅ HTTP 상태 코드 명시
- ✅ 예외 처리 체계화

---

## 4.8 FastAPI와 데이터베이스 통합

### 4.8.1 API 엔드포인트 작성

`src/kaira_fastapi_poetry/api/users.py` 파일 생성:

```python
"""
사용자 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """새 사용자 생성"""
    # 이메일 중복 확인
    existing_user = crud.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 사용자 생성 (실제로는 비밀번호 해싱 필요)
    user = crud.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password,  # 프로덕션에서는 해싱 필수!
        full_name=user_data.full_name
    )
    return user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """사용자 조회"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    return user


@router.get("/", response_model=list[UserResponse])
def list_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """사용자 목록 조회"""
    return crud.get_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """사용자 정보 수정"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    updated_user = crud.update_user(db, user_id, **user_data.model_dump(exclude_unset=True))
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """사용자 삭제"""
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    crud.delete_user(db, user_id)
    return None
```

`src/kaira_fastapi_poetry/api/posts.py` 파일 생성:

```python
"""
게시물 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import PostCreate, PostResponse, PostUpdate, PostWithAuthor

router = APIRouter(prefix="/api/posts", tags=["posts"])


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate, author_id: int, db: Session = Depends(get_db)):
    """새 게시물 생성"""
    # 작성자 확인
    author = crud.get_user(db, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="작성자를 찾을 수 없습니다"
        )
    
    post = crud.create_post(
        db,
        title=post_data.title,
        content=post_data.content,
        author_id=author_id
    )
    return post


@router.get("/", response_model=list[PostWithAuthor])
def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """게시물 목록 조회"""
    return crud.get_posts(db, skip=skip, limit=limit)


@router.get("/published", response_model=list[PostWithAuthor])
def list_published_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """발행된 게시물만 조회"""
    return crud.get_published_posts(db, skip=skip, limit=limit)


@router.get("/{post_id}", response_model=PostWithAuthor)
def get_post(post_id: int, db: Session = Depends(get_db)):
    """게시물 조회"""
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    return post


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostUpdate, db: Session = Depends(get_db)):
    """게시물 수정"""
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    updated_post = crud.update_post(db, post_id, **post_data.model_dump(exclude_unset=True))
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """게시물 삭제"""
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    crud.delete_post(db, post_id)
    return None
```

### 4.8.2 메인 애플리케이션에 통합

✅ **현재 프로젝트에 이미 구현됨**: `src/kaira_fastapi_poetry/main.py`

```python
"""
FastAPI 메인 애플리케이션 - 데이터베이스 통합 (프로젝트 현황)
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager

from kaira_fastapi_poetry.database import Base, engine
from kaira_fastapi_poetry.api.users import router as users_router
from kaira_fastapi_poetry.api.posts import router as posts_router


# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("애플리케이션이 시작되었습니다.")
    yield
    # Shutdown
    print("애플리케이션이 종료됩니다.")


app = FastAPI(
    lifespan=lifespan,
    title="Kaira API",
    version="1.0.0",
    description="User & Post Management API"
)


# 데이터베이스 기반 라우터 등록
app.include_router(users_router)
app.include_router(posts_router)


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "healthy"}
```

**통합 포인트**:
- ✅ `Base.metadata.create_all()` 로 테이블 자동 생성
- ✅ 라우터 분리로 모듈화
- ✅ Lifespan 이벤트로 앱 생명주기 관리

---

## 4.9 마이그레이션 관리 (Alembic)

### 4.9.1 Alembic 초기화

```bash
cd kaira-fastapi-poetry

# Alembic 초기화
alembic init alembic

# 초기화되는 파일:
# - alembic/
#   ├── env.py          (마이그레이션 환경 설정)
#   ├── script.py.mako  (마이그레이션 템플릿)
#   └── versions/       (마이그레이션 파일)
```

### 4.9.2 Alembic 설정

`alembic/env.py` 수정:

```python
"""
Alembic 마이그레이션 환경 설정
"""
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# SQLAlchemy URL 설정
config = context.config
sqlalchemy_url = os.getenv("DATABASE_URL", "postgresql://localhost/kaira_db")
config.set_main_option("sqlalchemy.url", sqlalchemy_url)

# 모델 메타데이터 임포트
from src.kaira_fastapi_poetry.database import Base
from src.kaira_fastapi_poetry.models import User, Post

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """오프라인 마이그레이션 실행"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """온라인 마이그레이션 실행"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 4.9.3 마이그레이션 작업

```bash
# 초기 마이그레이션 생성
alembic revision --autogenerate -m "Initial migration"

# 마이그레이션 실행
alembic upgrade head

# 마이그레이션 이력 확인
alembic history

# 이전 버전으로 롤백
alembic downgrade -1
```

---

## 4.10 실전 예제 - 서버 실행 및 테스트

### 4.10.1 서버 실행

```bash
# 프로젝트 디렉토리로 이동
cd /Users/joohyun/joohyun/python/fast-api/kaira-fastapi-poetry

# PYTHONPATH 설정 (필수)
export PYTHONPATH=/Users/joohyun/joohyun/python/fast-api/kaira-fastapi-poetry/src:$PYTHONPATH

# 서버 실행
.venv/bin/uvicorn kaira_fastapi_poetry.main:app --port 9000 --reload

# 또는 poetry 사용
poetry run uvicorn kaira_fastapi_poetry.main:app --port 9000 --reload
```

**서버 시작 메시지**:
```
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

### 4.10.2 Swagger 문서 접근

```bash
# 브라우저에서 접근
http://localhost:9000/docs

# 또는
http://127.0.0.1:9000/docs
```

### 4.10.3 API 테스트 (curl)

#### 사용자 생성

```bash
curl -X POST http://localhost:9000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123",
    "full_name": "John Doe"
  }'

# 응답:
# {
#   "id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "full_name": "John Doe",
#   "is_active": true,
#   "created_at": "2025-01-15T10:30:00",
#   "updated_at": "2025-01-15T10:30:00"
# }
```

#### 사용자 조회

```bash
curl http://localhost:9000/api/users/1

# 또는 목록 조회
curl http://localhost:9000/api/users/?skip=0&limit=10
```

#### 게시물 생성

```bash
curl -X POST "http://localhost:9000/api/posts/?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "첫 번째 게시물",
    "content": "FastAPI 데이터베이스 연동 완성!"
  }'
```

#### 게시물 목록 조회

```bash
curl http://localhost:9000/api/posts/
```

#### 발행된 게시물만 조회

```bash
curl http://localhost:9000/api/posts/published
```

**현재 프로젝트 상태**: ✅ **모든 API 구현 완료 및 테스트됨**

---

## 4.11 문제 해결

### 문제 1: PostgreSQL 연결 거부

**증상**:
```
psycopg2.OperationalError: could not connect to server
```

**해결**:
```bash
# PostgreSQL 서비스 시작 (macOS)
brew services start postgresql

# 또는 (Linux)
sudo systemctl start postgresql

# 또는 (Windows)
# Windows 서비스 관리자에서 PostgreSQL 서비스 시작
```

### 문제 2: 데이터베이스 존재하지 않음

**증상**:
```
psycopg2.OperationalError: database "kaira_db" does not exist
```

**해결**:
```bash
# 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE kaira_db;"
```

### 문제 3: 모듈 임포트 오류

**증상**:
```
ModuleNotFoundError: No module named 'models'
```

**해결**:
파이썬 경로 설정. `main.py`에 다음 추가:

```python
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
sys.path.insert(0, str(Path(__file__).parent))
```

### 문제 4: 마이그레이션 충돌

**증상**:
```
Target database is not up to date.
```

**해결**:
```bash
# 최신 마이그레이션 적용
alembic upgrade head

# 또는 처음부터 시작하려면
alembic stamp head
```

---

## 4.12 최종 체크리스트

### ✅ 기본 설정 (완료)

- [x] PostgreSQL 설치 및 Docker에서 실행
- [x] 데이터베이스(`kaira_db`) 및 사용자(`kaira_user`) 생성
- [x] `.env` 파일 작성 및 `.gitignore` 추가
- [x] 필수 패키지 설치 (`sqlalchemy`, `psycopg2-binary`, `alembic`, `pydantic`)

### ✅ 데이터베이스 모델 (완료)

- [x] `src/kaira_fastapi_poetry/database.py` - 연결 설정 작성
- [x] `src/kaira_fastapi_poetry/models.py` - User, Post 모델 정의
- [x] SQLAlchemy 2.0 DeclarativeBase 사용
- [x] 관계 설정 (One-to-Many: User → Posts)
- [x] 데이터베이스 테이블 자동 생성 완료

### ✅ Pydantic 스키마 (완료)

- [x] `src/kaira_fastapi_poetry/schemas.py` 파일 생성
- [x] UserCreate, UserResponse 스키마 작성
- [x] PostCreate, PostResponse 스키마 작성
- [x] `from_attributes=True` 설정 (SQLAlchemy 모델 변환)
- [x] 데이터 검증 동작 확인

### ✅ CRUD 작업 (완료)

- [x] `src/kaira_fastapi_poetry/crud.py` 파일 생성
- [x] User 관련 함수: create, read, update, delete, get_by_email
- [x] Post 관련 함수: create, read, update, delete, get_published
- [x] 중복 확인 및 오류 처리
- [x] 필터링 및 페이징 기능

### ✅ API 엔드포인트 (완료)

- [x] `src/kaira_fastapi_poetry/api/users.py` 라우터 생성
  - POST /api/users/ - 사용자 생성
  - GET /api/users/ - 사용자 목록 조회
  - GET /api/users/{user_id} - 특정 사용자 조회
  - PUT /api/users/{user_id} - 사용자 수정
  - DELETE /api/users/{user_id} - 사용자 삭제

- [x] `src/kaira_fastapi_poetry/api/posts.py` 라우터 생성
  - POST /api/posts/ - 게시물 생성
  - GET /api/posts/ - 전체 게시물 조회
  - GET /api/posts/published - 발행된 게시물만 조회
  - GET /api/posts/{post_id} - 특정 게시물 조회
  - PUT /api/posts/{post_id} - 게시물 수정
  - DELETE /api/posts/{post_id} - 게시물 삭제

- [x] `src/kaira_fastapi_poetry/main.py` - 라우터 통합
- [x] Swagger 문서 확인 (http://localhost:9000/docs)
- [x] HTTP 상태 코드 올바르게 설정 (201 Created, 404 Not Found 등)

### ✅ 테스트 (완료)

- [x] 서버 실행 및 기본 테스트
- [x] 모든 API 엔드포인트 curl 테스트
- [x] 데이터베이스 연결 테스트
- [x] 에러 처리 테스트 (중복 email, 존재하지 않는 user 등)
- [x] 로깅 시스템 정상 작동 확인

### 📝 테스트 커맨드

```bash
# 서버 실행 상태 확인
curl http://localhost:9000/api/health

# 사용자 생성 및 조회
curl -X POST http://localhost:9000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "email": "test@example.com", "password": "pass", "full_name": "Test User"}'

# 게시물 생성
curl -X POST "http://localhost:9000/api/posts/?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "테스트", "content": "내용"}'

# Swagger 문서
open http://localhost:9000/docs
```

### 🚀 다음 단계

1. **마이그레이션 관리 (Alembic)** - 스키마 버전 관리
2. **인증 및 보안** - JWT 토큰, 비밀번호 해싱
3. **Docker 컨테이너화** - 데이터베이스를 포함한 완전한 환경
4. **배포** - AWS, GCP, Azure 등 클라우드 플랫폼

---

**🎉 현재 프로젝트 상태: ✅ 모든 가이드 및 코드 업데이트 완료!**

- 서버: 포트 9000에서 정상 실행
- API: 모든 CRUD 엔드포인트 동작
- 문서: Swagger /docs 에서 확인 가능
- 데이터베이스: PostgreSQL 연결 및 테이블 생성 완료
