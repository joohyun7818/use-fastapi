from passlib.context import CryptContext
from datetime import datetime, timedelta
from uuid import uuid4
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
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

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
    sub: str  # subject: 사용자 이메일(유일값)
    # avoid mutable default lists, use Field with default_factory
    scopes: list[str] = Field(default_factory=list)

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
    
    # include issued-at and jti to ensure token uniqueness even when payload otherwise matches
    issued_at = datetime.utcnow()
    to_encode.update({"exp": expire, "iat": int(issued_at.timestamp()), "jti": str(uuid4())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """리프레시 토큰 생성 (더 긴 만료 시간)"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    issued_at = datetime.utcnow()
    to_encode.update({"exp": expire, "iat": int(issued_at.timestamp()), "jti": str(uuid4()), "type": "refresh"})
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


def build_token_response(access_token: str, refresh_token: Optional[str], expires_delta: Optional[timedelta]) -> Token:
    """Utility to build consistent token response object."""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires_in = int(expires_delta.total_seconds())
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", expires_in=expires_in)