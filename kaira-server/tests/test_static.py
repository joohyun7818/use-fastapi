# tests/test_static.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Kaira Static Server"}

def test_static_html_file():
    """정적 HTML 파일 접근 테스트"""
    response = client.get("/static/index.html")
  
    # 파일이 존재하면 200, 없으면 404
    if response.status_code == 200:
        assert "text/html" in response.headers["content-type"]
        assert len(response.content) > 0
    else:
        assert response.status_code == 404

def test_static_css_file():
    """정적 CSS 파일 접근 테스트"""
    response = client.get("/static/style.css")
  
    if response.status_code == 200:
        assert "text/css" in response.headers["content-type"]

