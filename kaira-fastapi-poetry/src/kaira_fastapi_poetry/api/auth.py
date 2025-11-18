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
    verify_token,
    SECRET_KEY,
    ALGORITHM,
)
from jose import jwt

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    사용자 로그인 및 토큰 발급 (이메일/비밀번호)
    
    폼 데이터:
    - username: 이메일 주소 (OAuth2 규격 이름 유지)
    - password: 비밀번호
    
    응답:
    - access_token: JWT 액세스 토큰
    - refresh_token: JWT 리프레시 토큰
    - token_type: "bearer"
    - expires_in: 만료 시간 (초)
    """
    email = form_data.username.strip()
    user = crud.get_user_by_email(db, email=email)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
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
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
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

@router.post("/refresh", response_model=Token)
async def refresh_token(
    payload: schemas.TokenRefreshRequest,
    db: Session = Depends(get_db)
):
    """
    리프레시 토큰으로 새로운 액세스 토큰 발급
    """
    refresh_token_value = payload.refresh_token
    
    # 리프레시 토큰 검증
    token_data = verify_token(refresh_token_value)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    # 토큰 타입 확인
    payload_data = jwt.decode(refresh_token_value, SECRET_KEY, algorithms=[ALGORITHM])
    if payload_data.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    
    # 사용자 확인
    user = crud.get_user_by_email(db, email=token_data.sub)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive",
        )
    
    # 새 액세스 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    }
