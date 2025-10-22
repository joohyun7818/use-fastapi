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
