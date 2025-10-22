import pytest

@pytest.fixture
def sample_data():
    '''테스트에서 사용할 샘플 데이터'''
    return {"name": "홍길동", "age": 30}


def test_sample_data(sample_data):
    '''fixture 사용 예제'''
    assert sample_data["name"] == "홍길동"
    assert sample_data["age"] == 30


