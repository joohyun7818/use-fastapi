"""
Pydantic 스키마 (API 요청/응답 검증)
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator


# ===== USER 스키마 =====

class UserBase(BaseModel):
    """사용자 기본 정보"""
    username: str = Field(..., min_length=1, max_length=50)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    full_name: Optional[str] = Field(None, max_length=100)


class UserCreate(UserBase):
    """사용자 생성 요청"""
    password: str = Field(..., min_length=8, max_length=255)
    
    @field_validator('password')
    @classmethod
    def password_must_be_strong(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('비밀번호는 대문자를 포함해야 합니다')
        return v


class UserUpdate(BaseModel):
    """사용자 수정 요청"""
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


class UserResponse(UserBase):
    """사용자 응답"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


# ===== POST 스키마 =====

class PostBase(BaseModel):
    """게시물 기본 정보"""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)


class PostCreate(PostBase):
    """게시물 생성 요청"""
    pass


class PostUpdate(BaseModel):
    """게시물 수정 요청"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    is_published: Optional[bool] = None


class PostResponse(PostBase):
    """게시물 응답"""
    id: int
    author_id: int
    is_published: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = {
        "from_attributes": True
    }


class PostWithAuthor(PostResponse):
    """작성자 정보를 포함한 게시물 응답"""
    author: UserResponse


class TokenRefreshRequest(BaseModel):
    """리프레시 요청 바디"""
    refresh_token: str = Field(..., min_length=1)
