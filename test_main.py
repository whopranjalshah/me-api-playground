from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def get_token():
    response = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    return response.json()["access_token"]

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200

def test_get_profiles():
    response = client.get("/api/v1/profiles")
    assert response.status_code == 200

def test_create_profile_needs_auth():
    response = client.post("/api/v1/profile", json={"name": "Test", "email": "test@test.com"})
    assert response.status_code == 401

def test_auth_login():
    response = client.post("/auth/token", data={"username": "admin", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in response.json()