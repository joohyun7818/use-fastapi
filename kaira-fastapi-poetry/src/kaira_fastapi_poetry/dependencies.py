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
    user = crud.get_user_by_email(db, email=token_data.sub)
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
