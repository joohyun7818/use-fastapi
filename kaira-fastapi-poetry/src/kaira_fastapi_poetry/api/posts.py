"""
게시물 API 엔드포인트
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import crud
from ..schemas import PostCreate, PostResponse, PostUpdate, PostWithAuthor

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
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/published", response_model=list[PostWithAuthor])
def list_published_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """발행된 게시물만 조회"""
    posts = crud.get_published_posts(db, skip=skip, limit=limit)
    return posts


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
    
    update_data = post_data.model_dump(exclude_unset=True)
    updated_post = crud.update_post(db, post_id, **update_data)
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
