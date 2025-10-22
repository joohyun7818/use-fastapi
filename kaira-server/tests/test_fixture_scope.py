"""
Pytest Fixture Scope 테스트

각 fixture의 scope별 실행 순서를 확인하는 테스트
실행: pytest tests/test_fixture_scope.py -v -s
"""

def test_function_1(function_fixture, module_fixture, session_fixture):
    """첫 번째 테스트"""
    print(f"테스트 1: function={function_fixture}, module={module_fixture}, session={session_fixture}")
    assert function_fixture == "function data"
    assert module_fixture == "module data"
    assert session_fixture == "session data"

def test_function_2(function_fixture, module_fixture, session_fixture):
    """두 번째 테스트 - function fixture는 새로 생성, module/session은 재사용"""
    print(f"테스트 2: function={function_fixture}, module={module_fixture}, session={session_fixture}")
    assert function_fixture == "function data"
    assert module_fixture == "module data"
    assert session_fixture == "session data"

def test_function_3(function_fixture, module_fixture, session_fixture):
    """세 번째 테스트"""
    print(f"테스트 3: function={function_fixture}, module={module_fixture}, session={session_fixture}")
    assert function_fixture == "function data"
    assert module_fixture == "module data"
    assert session_fixture == "session data"
