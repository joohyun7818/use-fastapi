"""
Docker PostgreSQL 연결 테스트
"""
import pytest
from sqlalchemy import text
from src.kaira_fastapi_poetry.database import engine


def test_database_connection():
    """데이터베이스 연결 테스트"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1 as test"))
        assert result.fetchone()[0] == 1
        print("✅ 데이터베이스 연결 성공!")


def test_postgresql_version():
    """PostgreSQL 버전 확인"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version()"))
        version_info = result.fetchone()[0]
        print(f"✅ PostgreSQL 정보: {version_info}")
        assert "PostgreSQL" in version_info


def test_database_user():
    """데이터베이스 사용자 확인"""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT current_user"))
        user = result.fetchone()[0]
        print(f"✅ 현재 사용자: {user}")
        assert user.lower() == "kaira_user"
