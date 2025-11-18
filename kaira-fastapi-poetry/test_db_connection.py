#!/usr/bin/env python3
"""
Docker PostgreSQL 연결 테스트 스크립트
"""
import sys
from pathlib import Path
from sqlalchemy import text

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from kaira_fastapi_poetry.database import engine

def test_database_connection():
    """데이터베이스 연결 테스트"""
    try:
        with engine.connect() as connection:
            print("✅ 데이터베이스 연결 성공!")
            
            # 간단한 쿼리 실행
            result = connection.execute(text("SELECT 1 as test"))
            print(f"✅ 쿼리 실행 성공: {result.fetchone()}")
            
            # PostgreSQL 버전 확인
            result = connection.execute(text("SELECT version()"))
            print(f"✅ PostgreSQL 정보: {result.fetchone()[0]}")
            
            return True
    except Exception as e:
        print(f"❌ 연결 실패: {type(e).__name__}")
        print(f"❌ 에러 메시지: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1)
