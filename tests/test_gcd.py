from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_gcd_12_18():
    r = client.get("/math/gcd?a=12&b=18")
    assert r.status_code == 200
    assert r.json() == {"a": 12, "b": 18, "gcd": 6}

def test_gcd_0_5():
    r = client.get("/math/gcd?a=0&b=5")
    assert r.status_code == 200
    assert r.json() == {"a": 0, "b": 5, "gcd": 5}

def test_gcd_7_13():
    r = client.get("/math/gcd?a=7&b=13")
    assert r.status_code == 200
    assert r.json() == {"a": 7, "b": 13, "gcd": 1}

def test_gcd_negative():
    r = client.get("/math/gcd?a=-1&b=5")
    assert r.status_code == 400
    assert r.json()["detail"]["error"] == "a and b must be non-negative"
