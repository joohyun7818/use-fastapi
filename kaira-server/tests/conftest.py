import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture(scope="function")
def function_fixture():
    '''각 테스트마다 실행(기본값)'''
    print("\n함수 fixture 시작")
    yield "function data"
    print("\n함수 fixture 종료")


@pytest.fixture(scope="module")
def module_fixture():
    '''모듈당 한번만 실행'''
    print("\n모듈 fixture 시작")
    yield "module data"
    print("\n모듈 fixture 종료")
    

@pytest.fixture(scope="session")
def session_fixture():
    '''모듈당 한번만 실행'''
    print("\n세션 fixture 시작")
    yield "session data"
    print("\n세션 fixture 종료")

@pytest.fixture(scope="module")
def test_client():
    '''모든 테스트에서 재사용할 TestClient'''
    with TestClient(app) as client:
        yield client
