from fastapi.testclient import TestClient
from kaira_fastapi_poetry.main import app
from uuid import uuid4

client = TestClient(app)


def test_refresh_returns_new_access_token():
    # unique email to avoid collisions
    unique = uuid4().hex[:8]
    email = f"test-{unique}@example.com"
    username = f"testuser{unique}"
    password = "Password123!"

    # register new user
    register_payload = {
        "username": username,
        "email": email,
        "password": password,
        "full_name": "Test User",
    }
    reg_resp = client.post("/api/auth/register", json=register_payload)
    assert reg_resp.status_code == 201

    # login for tokens
    login_data = {"username": email, "password": password}
    token_resp = client.post("/api/auth/token", data=login_data)
    assert token_resp.status_code == 200
    token_json = token_resp.json()
    access_token = token_json.get("access_token")
    refresh_token = token_json.get("refresh_token")
    assert access_token
    assert refresh_token

    # call refresh
    refresh_resp = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_resp.status_code == 200
    refresh_json = refresh_resp.json()
    new_access_token = refresh_json.get("access_token")
    assert new_access_token

    # the new access token should be different
    assert new_access_token != access_token
