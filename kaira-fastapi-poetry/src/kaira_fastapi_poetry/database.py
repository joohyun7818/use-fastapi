import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL 결정 로직:
# 1. .env 파일의 DATABASE_URL 사용
# 2. 없으면 환경변수 또는 Docker 네트워크에서 자동 구성
# 3. 개발 환경에서는 localhost, 컨테이너 환경에서는 postgres 사용
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://kaira_user:kaira_1234@postgres:5432/kaira_db"
    # ↑ Docker 네트워크 내에서 service name "postgres"로 접속
)

# Docker 컨테이너와의 연결을 위한 연결 풀 설정
engine = create_engine(
    DATABASE_URL,
    echo=True,
    # Docker 환경에서는 connection pooling 비활성화 권장
    poolclass=NullPool,
    # 연결 타임아웃 설정
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
    }
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()