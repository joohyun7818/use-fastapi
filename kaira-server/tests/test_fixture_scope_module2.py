"""
다른 모듈의 테스트 - module scope 비교용

이 파일의 테스트들은 test_fixture_scope.py와 별개의 모듈이므로:
- function_fixture: 각 테스트마다 새로 생성
- module_fixture: 이 모듈에서만 새로 생성 (다른 모듈의 것과 다름)
- session_fixture: 전체 세션에서 재사용 (같은 것)
"""

def test_module_2_test_1(function_fixture, module_fixture, session_fixture):
    """다른 모듈의 첫 테스트"""
    print(f"모듈2 테스트1: function={function_fixture}, module={module_fixture}, session={session_fixture}")
    assert function_fixture == "function data"

def test_module_2_test_2(function_fixture, module_fixture, session_fixture):
    """다른 모듈의 두 번째 테스트"""
    print(f"모듈2 테스트2: function={function_fixture}, module={module_fixture}, session={session_fixture}")
    assert function_fixture == "function data"
