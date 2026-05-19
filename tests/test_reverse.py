from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_reverse_hello():
    r = client.get("/strings/reverse?s=hello")
    assert r.status_code == 200
    assert r.json() == {"input": "hello", "reversed": "olleh"}

def test_reverse_missing():
    r = client.get("/strings/reverse")
    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "s is required"

def test_reverse_too_long():
    s = "a" * 1001
    r = client.get(f"/strings/reverse?s={s}")
    assert r.status_code == 413
    assert r.json()["detail"]["error"] == "too long"
