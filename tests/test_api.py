from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_api_returns_image():
    resp = client.post("/generate-meme", json={"error_log": "ZeroDivisionError: division by zero"})
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("image/")

def test_api_missing_field():
    resp = client.post("/generate-meme", json={})
    assert resp.status_code == 422

def test_api_invalid_data():
    resp = client.post("/generate-meme", data="bad", headers={"content-type": "application/json"})
    assert resp.status_code == 422
