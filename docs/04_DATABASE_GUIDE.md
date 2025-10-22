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

`src/kaira_fastapi_poetry/database.py` 파일 생성:

```python
"""
데이터베이스 연결 설정
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
    "postgresql://kaira_user:secure_password@localhost:5432/kaira_db"
)

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    echo=True,  # SQL 쿼리 출력 (개발 중만 사용)
    # future=True  # SQLAlchemy 2.0에서는 기본값
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# 모든 데이터베이스 모델의 기본 클래스
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

`src/kaira_fastapi_poetry/models.py` 파일 생성:

```python
"""
데이터베이스 모델 정의
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base


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

### 4.6.2 모델 생성 유틸리티

`src/kaira_fastapi_poetry/models/base.py`:

```python
"""
데이터베이스 테이블 초기화 유틸리티
"""
from database import Base, engine
from models import User, Post  # 모든 모델 임포트


def create_tables():
    """
    모든 테이블을 데이터베이스에 생성합니다.
    """
    print("테이블 생성 중...")
    Base.metadata.create_all(bind=engine)
    print("✅ 테이블 생성 완료!")


def drop_tables():
    """
    모든 테이블을 삭제합니다. (개발 중만 사용)
    """
    print("경고: 테이블 삭제 중...")
    Base.metadata.drop_all(bind=engine)
    print("✅ 테이블 삭제 완료!")


if __name__ == "__main__":
    create_tables()
```

테이블 생성 실행:

```bash
python -m src.kaira_fastapi_poetry.models.base
```

---

## 4.7 CRUD 작업 구현

### 4.7.1 CRUD 기초 함수

`src/kaira_fastapi_poetry/crud.py` 파일 생성:

```python
"""
CRUD (Create, Read, Update, Delete) 작업
"""
from sqlalchemy.orm import Session
from models import User, Post


# ===== USER CRUD =====

def get_user(db: Session, user_id: int):
    """ID로 사용자 조회"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """이메일로 사용자 조회"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """모든 사용자 조회 (페이징)"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, username: str, email: str, password_hash: str, full_name: str = None):
    """새 사용자 생성"""
    db_user = User(
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
            if value is not None:
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
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 10, author_id: int = None):
    """게시물 조회 (필터링, 페이징)"""
    query = db.query(Post)
    if author_id:
        query = query.filter(Post.author_id == author_id)
    return query.offset(skip).limit(limit).all()


def get_published_posts(db: Session, skip: int = 0, limit: int = 10):
    """발행된 게시물만 조회"""
    return db.query(Post).filter(Post.is_published == True).offset(skip).limit(limit).all()


def create_post(db: Session, title: str, content: str, author_id: int, is_published: bool = False):
    """새 게시물 생성"""
    db_post = Post(
        title=title,
        content=content,
        author_id=author_id,
        is_published=is_published
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, **kwargs):
    """게시물 정보 업데이트"""
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in kwargs.items():
            if value is not None:
                setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int):
    """게시물 삭제"""
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
```

### 4.7.2 Pydantic 스키마 정의

`src/kaira_fastapi_poetry/schemas.py` 파일 생성:

```python
"""
Pydantic 스키마 (API 요청/응답 검증)
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# ===== USER 스키마 =====

class UserBase(BaseModel):
    """사용자 기본 정보"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """사용자 생성 요청"""
    password: str


class UserUpdate(BaseModel):
    """사용자 수정 요청"""
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """사용자 응답"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ===== POST 스키마 =====

class PostBase(BaseModel):
    """게시물 기본 정보"""
    title: str
    content: str


class PostCreate(PostBase):
    """게시물 생성 요청"""
    pass


class PostUpdate(BaseModel):
    """게시물 수정 요청"""
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    """게시물 응답"""
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PostWithAuthor(PostResponse):
    """작성자 정보를 포함한 게시물 응답"""
    author: UserResponse
```

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

`src/kaira_fastapi_poetry/main.py` 수정:

```python
"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from api import users, posts

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Kaira FastAPI Service",
    description="정적 웹사이트 + 데이터베이스 연동",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="kaira-1.0.0"), name="static")

# API 라우터 등록
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
def root():
    """루트 엔드포인트"""
    return {
        "message": "Kaira FastAPI 서버",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """헬스 체크"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

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

## 4.10 실전 예제

### 4.10.1 전체 작업 흐름

```bash
# 1. 프로젝트 디렉토리로 이동
cd kaira-fastapi-poetry

# 2. 환경 변수 설정
cat > .env << EOF
DATABASE_URL=postgresql://kaira_user:secure_password@localhost:5432/kaira_db
DEBUG=True
EOF

# 3. 데이터베이스 테이블 생성
python -c "from src.kaira_fastapi_poetry.database import Base, engine; from src.kaira_fastapi_poetry.models import *; Base.metadata.create_all(bind=engine)"

# 4. 서버 실행
poetry run uvicorn src.kaira_fastapi_poetry.main:app --reload

# 5. API 문서 확인
open http://localhost:8000/docs
```

### 4.10.2 API 테스트 (curl)

```bash
# 사용자 생성
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password",
    "full_name": "John Doe"
  }'

# 응답:
# {
#   "id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "full_name": "John Doe",
#   "is_active": true,
#   "created_at": "2024-01-15T10:30:00",
#   "updated_at": "2024-01-15T10:30:00"
# }

# 게시물 생성
curl -X POST "http://localhost:8000/api/posts/?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "첫 번째 게시물",
    "content": "FastAPI 데이터베이스 연동 완성!"
  }'

# 게시물 목록 조회
curl http://localhost:8000/api/posts/

# 게시물 수정
curl -X PUT http://localhost:8000/api/posts/1 \
  -H "Content-Type: application/json" \
  -d '{
    "is_published": true
  }'

# 게시물 삭제
curl -X DELETE http://localhost:8000/api/posts/1
```

### 4.10.3 테스트 코드 작성

`tests/test_database.py`:

```python
"""
데이터베이스 API 테스트
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.kaira_fastapi_poetry.main import app, get_db
from src.kaira_fastapi_poetry.database import Base
from src.kaira_fastapi_poetry.models import User, Post

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown():
    """각 테스트마다 테이블 초기화"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user():
    """사용자 생성 테스트"""
    response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"


def test_get_user():
    """사용자 조회 테스트"""
    # 먼저 사용자 생성
    create_response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass"
        }
    )
    user_id = create_response.json()["id"]
    
    # 사용자 조회
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == "testuser"


def test_create_post():
    """게시물 생성 테스트"""
    # 사용자 생성
    user_response = client.post(
        "/api/users/",
        json={
            "username": "author",
            "email": "author@example.com",
            "password": "pass"
        }
    )
    user_id = user_response.json()["id"]
    
    # 게시물 생성
    response = client.post(
        f"/api/posts/?author_id={user_id}",
        json={
            "title": "테스트 게시물",
            "content": "테스트 내용"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "테스트 게시물"
    assert data["author_id"] == user_id
```

테스트 실행:

```bash
# 전체 테스트 실행
poetry run pytest tests/ -v

# 특정 테스트만 실행
poetry run pytest tests/test_database.py::test_create_user -v

# 커버리지 보고서
poetry run pytest tests/ --cov=src --cov-report=html
```

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

## 4.12 체크리스트

이 단계 완료 후 다음 항목을 확인하세요:

### ✅ 기본 설정
- [ ] PostgreSQL 설치 및 실행
- [ ] 데이터베이스 및 사용자 생성
- [ ] `.env` 파일 작성 및 `.gitignore` 추가
- [ ] 필수 패키지 설치 (`sqlalchemy`, `psycopg2-binary`, `alembic`)

### ✅ 데이터베이스 모델
- [ ] `database.py`에 연결 설정 작성
- [ ] `models.py`에 User, Post 모델 정의
- [ ] 데이터베이스 테이블 생성 확인
- [ ] 관계 설정 (One-to-Many) 확인

### ✅ CRUD 작업
- [ ] `crud.py`에 기본 CRUD 함수 작성
- [ ] `schemas.py`에 Pydantic 스키마 작성
- [ ] 데이터 검증 동작 확인

### ✅ API 엔드포인트
- [ ] 사용자 API 엔드포인트 작성 및 테스트
- [ ] 게시물 API 엔드포인트 작성 및 테스트
- [ ] Swagger 문서 (/docs) 확인
- [ ] HTTP 상태 코드 올바르게 설정

### ✅ 테스트
- [ ] `test_database.py` 작성
- [ ] 모든 테스트 통과 확인
- [ ] 테스트 커버리지 80% 이상

### ✅ 마이그레이션
- [ ] Alembic 초기화
- [ ] `env.py` 설정 완료
- [ ] 마이그레이션 파일 생성 및 적용
- [ ] 롤백 기능 테스트

### ✅ 배포 준비
- [ ] 프로덕션용 `DATABASE_URL` 설정
- [ ] 비밀번호 해싱 구현 (프로덕션 필수)
- [ ] 에러 로깅 설정
- [ ] 백업 전략 수립

---

## 다음 단계

**5단계: Docker 컨테이너화** (예정)
- 데이터베이스를 포함한 Docker 구성
- docker-compose로 다중 서비스 관리
- 로컬 개발 환경과 프로덕션 환경 분리

이 가이드가 도움이 되길 바랍니다! 🎉
