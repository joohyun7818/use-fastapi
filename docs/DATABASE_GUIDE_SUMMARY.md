# FastAPI 데이터베이스 가이드 요약

> **새로운 4단계 가이드 추가: 데이터베이스 연결 및 관리**

---

## 📋 가이드 개요

`04_DATABASE_GUIDE.md`는 FastAPI 애플리케이션에 데이터베이스를 연동하는 방법을 완벽하게 설명하는 가이드입니다.

**작성일**: 2025년 10월 22일  
**예상 학습 시간**: 5-7시간  
**난이도**: ⭐⭐ (중간)  
**선행 학습**: 1~3단계 완료 필수

---

## 🎯 주요 내용

### 1️⃣ 인기 있는 데이터베이스 연결 방법 3가지 비교

#### 🥇 SQLAlchemy + PostgreSQL (가장 권장) ⭐⭐⭐⭐⭐
- **특징**: 가장 널리 사용되는 조합
- **장점**: 강력한 ORM, 관계형 데이터베이스, 마이그레이션 지원, 프로덕션 준비 완료
- **단점**: 학습 곡선, PostgreSQL 설치 필요
- **적합한 프로젝트**: 복잡한 비즈니스 로직, 대규모 데이터, 마이크로서비스, 엔터프라이즈

#### 🥈 MongoDB + Motor (NoSQL) ⭐⭐⭐⭐
- **특징**: 비관계형 데이터베이스
- **장점**: 설정 간단, 빠른 프로토타입, 유연한 스키마, 수평 확장 용이
- **단점**: 복잡한 트랜잭션 미지원, 메모리 사용 많음
- **적합한 프로젝트**: 빠른 프로토타입, 로그 수집, 실시간 데이터

#### 🥉 SQLite (로컬/테스트) ⭐⭐
- **특징**: 파일 기반 가벼운 데이터베이스
- **장점**: 설치 불필요, 외부 의존성 없음, 학습하기 쉬움
- **단점**: 동시성 제한, 프로덕션 부적합
- **적합한 프로젝트**: 학습용, 개인 프로젝트, 프로토타입, 테스트

---

### 2️⃣ SQLAlchemy + PostgreSQL 선택 이유

이 가이드에서 **SQLAlchemy + PostgreSQL**을 선택한 이유:

1. **가장 인기 있는 조합** - 대부분의 실제 FastAPI 프로젝트 사용
2. **프로덕션 준비 완료** - 대규모 애플리케이션에 적합
3. **강력한 도구 지원** - Alembic 마이그레이션, pytest-sqlalchemy 등
4. **채용 시장** - 기술 습득이 경력에 직결
5. **다른 DB로의 전환 용이** - 기초를 잘 배우면 다른 것도 쉬움

---

### 3️⃣ 주요 학습 섹션

#### 4.4 환경 설정
- PostgreSQL 설치 (macOS, Linux, Windows)
- 데이터베이스 및 사용자 생성
- Python 패키지 설치 (sqlalchemy, psycopg2-binary, alembic)
- 환경 변수 관리 (.env 파일)

#### 4.5 SQLAlchemy 기초
- 데이터베이스 연결 설정
- 엔진(Engine), 세션(Session), 베이스(Base) 이해
- 의존성 주입을 통한 세션 제공

#### 4.6 데이터베이스 모델 정의
- SQLAlchemy 모델 작성 (User, Post 예제)
- 관계 설정 (One-to-Many, Many-to-Many)
- 테이블 생성

#### 4.7 CRUD 작업 구현
- **Create**: 데이터 생성
- **Read**: 데이터 조회 (필터링, 페이징)
- **Update**: 데이터 수정
- **Delete**: 데이터 삭제

#### 4.8 FastAPI와 데이터베이스 통합
- Pydantic 스키마 정의
- API 엔드포인트 작성 (사용자, 게시물 예제)
- 요청 검증 및 응답 직렬화
- HTTP 상태 코드 관리

#### 4.9 마이그레이션 관리 (Alembic)
- Alembic 초기화
- 자동 마이그레이션 파일 생성
- 마이그레이션 실행 및 롤백
- 버전 관리

#### 4.10 실전 예제
- 전체 작업 흐름 (환경 설정 → 테스트)
- API 테스트 (curl 명령어)
- 테스트 코드 작성 (pytest)

---

## 💻 실전 예제 미리보기

### 데이터베이스 모델 정의

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class User(Base):
    """사용자 모델"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")

class Post(Base):
    """게시물 모델"""
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_published = Column(Boolean, default=False)
    
    author = relationship("User", back_populates="posts")
```

### API 엔드포인트 통합

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud
from schemas import UserCreate, UserResponse

router = APIRouter(prefix="/api/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """새 사용자 생성"""
    existing_user = crud.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    user = crud.create_user(
        db,
        username=user_data.username,
        email=user_data.email,
        password_hash=user_data.password,
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
```

### 테스트 코드

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 테스트용 SQLite 데이터베이스
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def test_create_user():
    """사용자 생성 테스트"""
    response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
```

---

## 🛠️ 필수 설치 패키지

```bash
poetry add sqlalchemy psycopg2-binary alembic python-dotenv pydantic-settings
```

| 패키지 | 버전 | 용도 |
|--------|------|------|
| sqlalchemy | ^2.0 | ORM 라이브러리 |
| psycopg2-binary | ^2.9 | PostgreSQL 어댑터 |
| alembic | ^1.12 | 마이그레이션 도구 |
| python-dotenv | ^1.0 | 환경 변수 관리 |
| pydantic-settings | ^2.0 | Pydantic 설정 |

---

## 🗺️ 학습 경로

```
1단계: FastAPI-CLI (기초)
   ↓
2단계: Poetry (의존성 관리)
   ↓
3단계: 테스트와 로깅
   ↓
4단계: 데이터베이스 연결 ← 새 가이드
   ↓
5단계: Docker 컨테이너화
   ↓
6단계: 클라우드 배포
```

---

## 📊 변경 사항 요약

### 파일 구조 변경

```
docs/
├── 01_FASTAPI_CLI_GUIDE.md           (변경 없음)
├── 02_POETRY_GUIDE.md                (변경 없음)
├── 03_TESTING_LOGGING_GUIDE.md       (변경 없음)
├── 04_DATABASE_GUIDE.md              ⭐ NEW! (새로 추가)
├── 05_DOCKER_GUIDE.md                (이전 04_DOCKER_GUIDE.md)
└── 06_CLOUD_DEPLOYMENT_GUIDE.md      (이전 05_CLOUD_DEPLOYMENT_GUIDE.md)
```

### 업데이트된 파일

- ✅ `INDEX.md` - 4단계 데이터베이스 가이드 추가
- ✅ `GUIDE_STRUCTURE.txt` - 문서 구조 업데이트
- ✅ `LEARNING_ROADMAP.md` - 전체 로드맵 업데이트

---

## 🎯 다음 단계

1. **지금**: `04_DATABASE_GUIDE.md` 읽기 시작
2. **4.4절부터**: PostgreSQL 설치 및 환경 설정
3. **4.6절부터**: 데이터 모델 정의 및 테이블 생성
4. **4.8절부터**: API 엔드포인트 작성
5. **4.10절부터**: 전체 시스템 테스트

---

## 📚 추천 학습 순서

**처음 배우는 경우**:
1. 4.2 - 3가지 방식 이해 및 비교
2. 4.3 - SQLAlchemy + PostgreSQL 선택 이유
3. 4.4 - 환경 설정 (PostgreSQL 설치)
4. 4.5 - SQLAlchemy 기초
5. 4.6 - 모델 정의
6. 4.7 - CRUD 작업
7. 4.8 - API 통합
8. 4.9 - 마이그레이션
9. 4.10 - 실전 예제 및 테스트

**이미 데이터베이스를 알고 있는 경우**:
- 4.4 - 환경 설정만 확인
- 4.5 ~ 4.8 - 빠르게 진행
- 4.10 - 실전 예제로 복습

---

## ✅ 체크리스트

완료 후 확인할 항목:

- [ ] PostgreSQL 설치 및 실행 확인
- [ ] 데이터베이스 생성 및 사용자 생성
- [ ] 모델 정의 및 테이블 생성
- [ ] CRUD 함수 작성
- [ ] API 엔드포인트 작성 및 테스트
- [ ] 테스트 코드 작성
- [ ] Alembic 마이그레이션 설정
- [ ] 모든 curl 명령어 실행 및 동작 확인

---

## 🔗 참고 자료

- [FastAPI 공식 문서 - 데이터베이스](https://fastapi.tiangolo.com/ko/tutorial/sql-databases/)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [PostgreSQL 공식 문서](https://www.postgresql.org/docs/)
- [Alembic 문서](https://alembic.sqlalchemy.org/)

---

## 🎉 완성!

이제 FastAPI 프로젝트는 다음과 같은 기능을 가지게 됩니다:

```
FastAPI 서버
├── 정적 파일 서빙 (1단계)
├── Poetry 의존성 관리 (2단계)
├── 테스트 및 로깅 (3단계)
├── PostgreSQL 데이터베이스 연동 (4단계) ← NEW!
├── Docker 컨테이너화 (5단계)
└── 클라우드 배포 준비 (6단계)
```

**다음 단계**: 5단계 - Docker 컨테이너화로 진행하세요!
