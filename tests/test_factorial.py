import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_factorial_0():
    response = client.get("/math/factorial?n=0")
    assert response.status_code == 200
    assert response.json() == {"n": 0, "result": 1}

def test_factorial_5():
    response = client.get("/math/factorial?n=5")
    assert response.status_code == 200
    assert response.json() == {"n": 5, "result": 120}

def test_factorial_20():
    response = client.get("/math/factorial?n=20")
    assert response.status_code == 200
    assert response.json() == {"n": 20, "result": 2432902008176640000}

def test_factorial_negative():
    response = client.get("/math/factorial?n=-1")
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "n must be 0-20"}}

def test_factorial_too_large():
    response = client.get("/math/factorial?n=21")
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "n must be 0-20"}}