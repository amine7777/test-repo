from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_factorial_success():
    response = client.get("/factorial", params={"n": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 120}

def test_factorial_invalid():
    response = client.get("/factorial", params={"n": -3})
    assert response.status_code == 400
    assert response.json()["detail"] == "n must be non‑negative"
