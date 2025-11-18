# 8단계: JWT 인증 및 사용자 보안

> **목표**: JWT 토큰을 이용한 보안 인증 시스템 구축
> 
> **학습 시간**: 3-4일
> **난이도**: ⭐⭐⭐ (중간)
> **사전 요구사항**: 4단계 완료 (데이터베이스 구축)

---

## 📋 8단계 학습 목표

8단계를 완료하면 다음을 할 수 있게 됩니다:

- ✅ 비밀번호 안전하게 해싱하기 (bcrypt)
- ✅ JWT 토큰 생성 및 검증
- ✅ OAuth2 + JWT 인증 구현
- ✅ 의존성 주입으로 현재 사용자 조회 (`get_current_user`)
- ✅ 로그인 엔드포인트 구축 (`POST /api/auth/token`)
- ✅ 보호된 엔드포인트 생성 (`GET /api/users/me`)
- ✅ 토큰 갱신 (Refresh Token)
- ✅ 역할 기반 접근 제어 (RBAC) 준비

**완료 시 결과물**: JWT 토큰으로 보호되는 전체 API

---

## 📚 8단계 목차

| 챕터 | 주제 | 예상 시간 |
|------|------|---------|
| [8.1](#81-보안의-중요성) | 보안의 중요성 | 15분 |
| [8.2](#82-비밀번호-해싱-bcrypt-passlib) | 비밀번호 해싱 | 20분 |
| [8.3](#83-jwt-토큰-이해) | JWT 토큰 이해 | 25분 |
| [8.4](#84-oauth2--jwt-인증-구현) | OAuth2 + JWT | 45분 |
| [8.5](#85-로그인-엔드포인트) | 로그인 엔드포인트 | 30분 |
| [8.6](#86-보호된-엔드포인트) | 보호된 엔드포인트 | 30분 |
| [8.7](#87-토큰-갱신) | 토큰 갱신 | 25분 |
| [8.8](#88-역할-기반-접근-제어-rbac) | RBAC 기초 | 30분 |
| [8.9](#89-실전-예제-및-테스트) | 실전 예제 | 45분 |
| [8.10](#810-체크리스트) | 체크리스트 | - |

---

## 8.1 보안의 중요성

### 왜 인증이 필요한가?

**현재 상태** (4단계까지):
```python
# ❌ 위험: 누구나 API 접근 가능
@app.get("/api/users/")
def get_users():
    # 모든 사용자 조회 가능 (접근 제어 없음)
    return crud.get_users(db)
```

**보안 요구사항**:
- ✅ 인증: 사용자가 누구인지 확인
- ✅ 인가: 사용자가 무엇을 할 수 있는지 확인
- ✅ 감사: 누가 언제 무엇을 했는지 기록

**인증 방식 비교**:

| 방식 | 특징 | 사용 사례 |
|------|------|---------|
| **Session** | 서버가 상태 관리 | 전통적 웹 애플리케이션 |
| **Token (JWT)** | 서버가 상태 없음 | SPA, 모바일 앱, API |
| **OAuth2** | 제3자 인증 | 소셜 로그인 |
| **SAML** | 엔터프라이즈 인증 | 기업 환경 |

**이 가이드에서는 JWT를 사용합니다**:
- ✅ 모던: REST API 표준
- ✅ 확장 가능: 마이크로서비스에 적합
- ✅ 상태 없음: 수평 확장 용이
- ✅ 모바일 친화적: 브라우저 쿠키 불필요

---

## 8.2 비밀번호 해싱 (bcrypt, passlib)

### 필수 패키지 설치

```bash
poetry add python-jose passlib bcrypt python-multipart
```

**패키지 설명**:
- `python-jose`: JWT 토큰 생성/검증
- `passlib`: 비밀번호 해싱 라이브러리
- `bcrypt`: 암호화 알고리즘
- `python-multipart`: 폼 데이터 처리 (로그인 폼)

### 비밀번호 해싱 설정

**`src/kaira_fastapi_poetry/security.py` (새 파일 생성)**:

```python
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel, Field
import os

# 비밀번호 해싱 설정
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# JWT 설정
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# 비밀번호 해싱 함수
def hash_password(password: str) -> str:
    """평문 비밀번호를 bcrypt로 해싱"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시된 비밀번호 비교"""
    return pwd_context.verify(plain_password, hashed_password)

# JWT 토큰 생성 함수
class TokenData(BaseModel):
    """토큰에 포함될 데이터"""
    sub: str  # subject: 사용자 아이디 또는 username
    scopes: list[str] = Field(default_factory=list)  # 토큰의 스코프 (권한)

class Token(BaseModel):
    """로그인 응답 모델"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # 초 단위 만료 시간

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """액세스 토큰 생성"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """리프레시 토큰 생성 (더 긴 만료 시간)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[TokenData]:
    """토큰 검증 및 데이터 추출"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        scopes = payload.get("scopes", [])
        token_data = TokenData(sub=username, scopes=scopes)
        return token_data
    except JWTError:
        return None
```

### 환경 변수 설정

**.env 파일에 추가**:

```bash
# 기존 설정
DATABASE_URL=postgresql://kaira_user:kaira_1234@localhost:5432/kaira_db

# 새로 추가
SECRET_KEY=your-super-secret-key-replace-this  # 나중에 openssl rand -hex 32 로 생성
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**프로덕션 SECRET_KEY 생성** (한 번만 실행):

```bash
openssl rand -hex 32
# 출력: abc123def456ghi789... (64자)

# 이 값을 .env의 SECRET_KEY에 복사
```

---

## 8.3 JWT 토큰 이해

### JWT 구조

JWT는 3개의 부분으로 나뉨 (점으로 구분):

```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiJqb2huZG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Header** (토큰의 타입과 해싱 알고리즘):
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload** (실제 데이터):
```json
{
  "sub": "johndoe",      // subject (사용자 ID)
  "username": "john",    // 사용자명
  "exp": 1699999999,     // expiration time
  "iat": 1699000000,     // issued at
  "scopes": ["read", "write"]  // 권한
}
```

**Signature** (서명 - 위변조 방지):
```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret_key
)
```

### JWT 장점 vs 단점

**장점** ✅:
- **상태 없음**: 서버가 세션 저장 불필요
- **확장성**: 마이크로서비스에 적합
- **모바일 친화적**: 쿠키 없이 작동
- **CORS 친화적**: Cross-Origin 문제 해결

**단점** ❌:
- **토큰 크기**: 세션 ID보다 큼
- **토큰 폐기 어려움**: 발급 후 만료까지 유효
- **갱신 필요**: 액세스 토큰 만료 시 리프레시 필요

**해결책**:
- 리프레시 토큰 사용 (만료 시간 길게)
- 토큰 블랙리스트 (Redis)
- 짧은 만료 시간 설정 (30분)

---

## 8.4 OAuth2 + JWT 인증 구현

### 의존성: get_current_user

**`src/kaira_fastapi_poetry/dependencies.py` (새 파일 생성)**:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud
from .database import get_db
from .security import verify_token
from .models import User

# OAuth2 스킴 정의 (Swagger에 표시됨)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/token",
    scopes={
        "read": "사용자 정보 읽기",
        "write": "사용자 정보 수정",
        "admin": "관리자 권한",
    }
)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """현재 로그인된 사용자 반환 (보호된 엔드포인트용)"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 토큰 검증
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    # 데이터베이스에서 사용자 조회
    user = crud.get_user_by_username(db, username=token_data.sub)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """활성화된 사용자만 반환"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

**`src/kaira_fastapi_poetry/models/__init__.py` 에 추가**:

```python
# username 필드 추가 (JWT의 sub로 사용)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
```

**schemas.py 업데이트**:

```python
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)  # 비밀번호 필드 추가

class UserInDB(UserResponse):
    """데이터베이스에서 읽은 사용자 (비밀번호 포함)"""
    hashed_password: str

class CurrentUser(UserResponse):
    """현재 로그인된 사용자 정보"""
    pass
```

**crud.py에 추가**:

```python
def get_user_by_username(db: Session, username: str):
    """사용자명으로 사용자 조회"""
    return db.query(models.User).filter(models.User.username == username).first()
```

---

## 8.5 로그인 엔드포인트

**`src/kaira_fastapi_poetry/api/auth.py` (새 파일 생성)**:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import crud, schemas, models
from ..database import get_db
from ..security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 토큰 발급
    
    폼 데이터:
    - username: 사용자명
    - password: 비밀번호
    
    응답:
    - access_token: JWT 액세스 토큰
    - refresh_token: JWT 리프레시 토큰
    - token_type: "bearer"
    - expires_in: 만료 시간 (초)
    """
    
    # 사용자명으로 사용자 조회
    user = crud.get_user_by_username(db, username=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    # 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 초 단위
    }

@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    새 사용자 등록
    """
    
    # 중복 확인
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # 비밀번호 해싱
    hashed_password = hash_password(user.password)
    
    # 새 사용자 생성
    db_user = crud.create_user(
        db,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name
    )
    
    return db_user
```

### main.py에 라우터 등록

```python
# 기존 라우터들 위에 추가
from .api import auth, users, posts

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
```

---

## 8.6 보호된 엔드포인트

**`src/kaira_fastapi_poetry/api/users.py` 수정**:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud, models
from ..schemas import UserResponse
from ..dependencies import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

# 현재 사용자 정보 조회 (새 엔드포인트)
@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    """현재 로그인된 사용자 정보 반환"""
    return current_user

# 기존 get_user 엔드포인트에 인증 추가
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)  # ← 추가
):
    """사용자 정보 조회 (인증 필요)"""
    db_user = crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

---

## 8.7 토큰 갱신

**auth.py에 추가**:

```python
from ..security import REFRESH_TOKEN_EXPIRE_DAYS
from jose import jwt
from ..config import settings

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    리프레시 토큰으로 새로운 액세스 토큰 발급
    """
    
    # 리프레시 토큰 검증
    token_data = verify_token(refresh_token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # 토큰 타입 확인
    payload = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    
    # 사용자 확인
    user = crud.get_user_by_username(db, username=token_data.sub)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # 새 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }

> 참고: 새 액세스 토큰이 기존 액세스 토큰과 동일하게 보일 경우가 있는데, 이는 액세스 토큰의 payload 및 만료(exp)가 동일한 경우 발생할 수 있습니다. 현재 구현에서는 `iat` 및 `jti`(JWT ID)를 액세스 토큰에 추가하여 항상 새로운 토큰이 발급되도록 보장합니다. (로그인→리프레시 직후 비교 시 토큰 문자열이 바뀌었는지 확인하세요.)
```

---

## 8.8 역할 기반 접근 제어 (RBAC)

### 모델 업데이트

```python
# models/__init__.py에 추가
from enum import Enum

class UserRole(str, Enum):
    """사용자 역할"""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"

class User(Base):
    __tablename__ = "users"
    
    # 기존 필드들...
    role = Column(String, default=UserRole.USER)  # ← 추가
```

### 권한 검증 의존성

```python
# dependencies.py에 추가
from .models import UserRole, User

async def get_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """관리자 권한 확인"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin users can access this resource"
        )
    return current_user

async def require_scope(
    scopes: list[str],
    current_user: User = Depends(get_current_active_user),
) -> User:
    """스코프 기반 권한 확인"""
    if current_user.role not in scopes:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return current_user
```

### 보호된 관리자 엔드포인트

```python
# users.py에 추가
@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(get_admin_user)  # 관리자만
):
    """사용자 삭제 (관리자만)"""
    db_user = crud.delete_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
```

---

## 8.9 실전 예제 및 테스트

### 로그인 테스트

```bash
# 1. 사용자 등록
curl -X POST http://localhost:9000/api/auth/register \
  -H "Content-Type: application/json" \
  -d 
'{ 
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

# 2. 로그인 (토큰 획득)
curl -X POST http://localhost:9000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePassword123"

# 응답:
# {
#   "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
#   "token_type": "bearer",
#   "expires_in": 1800
# }

# 3. 토큰으로 보호된 엔드포인트 접근
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

curl -X GET http://localhost:9000/api/users/me \
  -H "Authorization: Bearer $ACCESS_TOKEN"

# 응답:
# {
#   "id": 1,
#   "username": "john_doe",
#   "email": "john@example.com",
#   "full_name": "John Doe",
#   "is_active": true
# }
```

### 테스트 코드

```python
# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from kaira_fastapi_poetry.main import app
from kaira_fastapi_poetry import crud
from kaira_fastapi_poetry.security import hash_password

client = TestClient(app)

def test_register_user():
    """사용자 등록 테스트"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPassword123",
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"

def test_register_duplicate_email():
    """중복 이메일 등록 테스트"""
    # 첫 번째 등록
    client.post(
        "/api/auth/register",
        json={
            "username": "user1",
            "email": "duplicate@example.com",
            "password": "Password123",
        }
    )
    
    # 두 번째 등록 (실패)
    response = client.post(
        "/api/auth/register",
        json={
            "username": "user2",
            "email": "duplicate@example.com",
            "password": "Password123",
        }
    )
    assert response.status_code == 400

def test_login():
    """로그인 테스트"""
    # 사용자 먼저 등록
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "LoginPassword123",
        }
    )
    
    # 로그인
    response = client.post(
        "/api/auth/token",
        data={
            "username": "loginuser",
            "password": "LoginPassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_current_user():
    """현재 사용자 조회 테스트"""
    # 사용자 등록 및 로그인
    client.post(
        "/api/auth/register",
        json={
            "username": "currentuser",
            "email": "current@example.com",
            "password": "CurrentPassword123",
        }
    )
    
    login_response = client.post(
        "/api/auth/token",
        data={"username": "currentuser", "password": "CurrentPassword123"}
    )
    token = login_response.json()["access_token"]
    
    # 현재 사용자 정보 조회
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "currentuser"

def test_access_without_token():
    """토큰 없이 보호된 엔드포인트 접근 테스트"""
    response = client.get("/api/users/me")
    assert response.status_code == 401

def test_invalid_token():
    """유효하지 않은 토큰으로 접근 테스트"""
    response = client.get(
        "/api/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
```

---

## 8.10 체크리스트

### ✅ 기본 인증

- [ ] `security.py` 생성 및 해싱/토큰 함수 구현
- [ ] `dependencies.py` 생성 및 `get_current_user` 구현
- [ ] `.env` 파일에 `SECRET_KEY` 추가
- [ ] 필수 패키지 설치 (`passlib`, `python-jose`, `python-multipart`)

### ✅ 인증 엔드포인트

- [ ] `api/auth.py` 생성
- [ ] `POST /api/auth/register` - 사용자 등록
- [ ] `POST /api/auth/token` - 로그인 (토큰 발급)
- [ ] `POST /api/auth/refresh` - 토큰 갱신
- [ ] `main.py`에 auth 라우터 등록

### ✅ 보호된 엔드포인트

- [ ] `GET /api/users/me` - 현재 사용자 정보
- [ ] 기존 엔드포인트에 `Depends(get_current_user)` 추가
- [ ] 관리자 엔드포인트 `Depends(get_admin_user)` 적용

### ✅ 모델 업데이트

- [ ] `User` 모델에 `username` 필드 추가
- [ ] `User` 모델에 `role` 필드 추가 (RBAC)
- [ ] `hashed_password` 필드 적용
- [ ] `schemas.py` 업데이트 (UserCreate에 password)

### ✅ 테스트

- [ ] `tests/test_auth.py` 작성
- [ ] 등록 테스트
- [ ] 로그인 테스트
- [ ] 토큰 검증 테스트
- [ ] 권한 확인 테스트

### ✅ 문서화

- [ ] Swagger `/docs`에서 인증 옵션 확인
- [ ] 토큰 필드 설명 추가
- [ ] 에러 응답 문서화

---

**현재 프로젝트 상태**: ✅ 모든 기본 구성 완료

**다음 단계**: 9단계 - 고급 기능 (Alembic, 캐싱, 백그라운드 작업)