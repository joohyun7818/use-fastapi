"""
데이터베이스 테이블 초기화 유틸리티
"""
from ..database import Base, engine
from ..models import User, Post  # 모든 모델 임포트


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