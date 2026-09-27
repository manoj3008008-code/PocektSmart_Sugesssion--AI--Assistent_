import os
os.environ["USE_MOCK_AI"] = "true"
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register_login_and_home():
    email = "test_pocketsmart@example.com"
    r = client.post("/api/register", json={"name":"Test User","email":email,"password":"secret123"})
    assert r.status_code in (200, 409)
    r = client.post("/api/login", json={"email":email,"password":"secret123"})
    assert r.status_code == 200
    r = client.post("/api/generate-home", json={
        "budget":50000,
        "rooms":["Living Room"],
        "items":[{"category":"lighting","item":"ceiling lights","quantity":2,"priority":"high"}],
        "style":"modern","city":"Chennai"
    })
    assert r.status_code == 200
    assert r.json()["planner"] == "home"
