from app.main import app

def test_get_existing_item(test_client):
    """존재하는 아이템 조회"""
    response = test_client.get("/items/item1")
    assert response.status_code == 200
    assert response.json()["name"] == "book"

def test_get_nonexistent_item(test_client):
    """존재하지 않는 아이템 조회"""
    response = test_client.get("/items/item999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_error_header_in_response(test_client):
    """오류 응답에 커스텀 헤더 포함 여부 확인"""
    response = test_client.get("/items-header/item999")
    assert response.status_code == 404
    assert response.headers.get("X-Error") == "Custom error header"

def test_custom_exception_error(test_client):
    """커스텀 예외 핸들러 테스트"""
    response = test_client.get("/custom-items/item999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] == "ItemNotFound"
    assert "item999" in data["message"]
    assert "suggestion" in data

def test_custom_exception_not_error(test_client):
    """커스텀 예외 핸들러 테스트(정상작동)"""
    response = test_client.get("/custom-items/item1")
    assert response.status_code == 200
    data = response.json()
    assert "item1" == data["item_id"]

def test_validation_error(test_client):
    """검증 에러 커스터마이징 테스트"""
    response = test_client.post(
        "/validated-items/",
        json={"name": "책", "price": "invalid"}  # 잘못된 타입
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"] == "ValidationError"
    assert "details" in data
    assert len(data["details"]) > 0