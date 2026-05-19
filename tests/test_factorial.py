from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_factorial_zero():
    r = client.get("/math/factorial?n=0")
    assert r.status_code == 200
    assert r.json() == {"n": 0, "result": 1}

def test_factorial_five():
    r = client.get("/math/factorial?n=5")
    assert r.status_code == 200
    assert r.json() == {"n": 5, "result": 120}

def test_factorial_twenty():
    r = client.get("/math/factorial?n=20")
    assert r.status_code == 200
    assert r.json() == {"n": 20, "result": 2432902008176640000}

def test_factorial_negative():
    r = client.get("/math/factorial?n=-1")
    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "n must be 0-20"

def test_factorial_twenty_one():
    r = client.get("/math/factorial?n=21")
    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "n must be 0-20"
