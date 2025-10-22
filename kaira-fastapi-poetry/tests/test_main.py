# tests/test_main.py
from fastapi.testclient import TestClient
from kaira_fastapi_poetry.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
