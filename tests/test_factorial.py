import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_factorial_zero():
    response = client.get("/factorial", params={"n": 0})
    assert response.status_code == 200
    assert response.json() == {"result": 1}

def test_factorial_positive():
    response = client.get("/factorial", params={"n": 5})
    assert response.status_code == 200
    assert response.json() == {"result": 120}

def test_factorial_one():
    response = client.get("/factorial", params={"n": 1})
    assert response.status_code == 200
    assert response.json() == {"result": 1}

def test_factorial_large():
    response = client.get("/factorial", params={"n": 10})
    assert response.status_code == 200
    assert response.json() == {"result": 3628800}

def test_factorial_negative():
    response = client.get("/factorial", params={"n": -1})
    assert response.status_code == 400
    assert "non-negative" in response.json()["detail"]

def test_factorial_exceeds_max():
    response = client.get("/factorial", params={"n": 1001})
    assert response.status_code == 400
    assert "1000" in response.json()["detail"]

def test_factorial_invalid_type():
    response = client.get("/factorial", params={"n": "abc"})
    assert response.status_code == 422
