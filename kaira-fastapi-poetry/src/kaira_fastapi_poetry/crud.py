"""
CRUD (Create, Read, Update, Delete) 작업
"""
from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models


# ===== USER CRUD =====

def get_user(db: Session, user_id: int):
    """ID로 사용자 조회"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """이메일로 사용자 조회"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    """사용자명으로 사용자 조회"""
    return db.query(models.User).filter(models.User.username == username).first()


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


def get_published_posts(db: Session, skip: int = 0, limit: int = 10):
    """발행된 게시물만 조회"""
    return db.query(models.Post).filter(
        models.Post.is_published == True
    ).offset(skip).limit(limit).all()


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


def update_post(db: Session, post_id: int, **kwargs):
    """게시물 정보 업데이트"""
    db_post = get_post(db, post_id)
    if db_post:
        for key, value in kwargs.items():
            if value is not None and hasattr(db_post, key):
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
