from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to kaira Server!", "status": "ok"}

def test_get_item():
    response = client.get("/api/items/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42

def test_create_item():
    '''아이템 생성 테스트'''
    response = client.post(
        "/items/",
        json={"name": "책", "price": 15000, "is_offer": True}
    )
    assert response.status_code == 200
    data = response.json()
   
    assert data["item"]["name"] == "책"
    assert data["item"]["price"] == 15000
    assert data["message"] == "Item created"

def test_headers():
    """헤더 전송 테스트"""
    response = client.get(
        "/headers/",
        headers={
            "User-Agent": "TestClient",
            "X-Token": "secret-token"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["User-Agent"] == "TestClient"
    assert data["X-Token"] == "secret-token"

def test_read_root(test_client):
    '''fixture 사용'''
    response = test_client.get("/")
    assert response.status_code == 200
