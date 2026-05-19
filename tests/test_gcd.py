import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_gcd_basic():
    response = client.get("/math/gcd?a=12&b=8")
    assert response.status_code == 200
    assert response.json() == {"a": 12, "b": 8, "gcd": 4}

def test_gcd_coprime():
    response = client.get("/math/gcd?a=7&b=13")
    assert response.status_code == 200
    assert response.json() == {"a": 7, "b": 13, "gcd": 1}

def test_gcd_zero():
    response = client.get("/math/gcd?a=0&b=5")
    assert response.status_code == 200
    assert response.json() == {"a": 0, "b": 5, "gcd": 5}

def test_gcd_same_numbers():
    response = client.get("/math/gcd?a=15&b=15")
    assert response.status_code == 200
    assert response.json() == {"a": 15, "b": 15, "gcd": 15}

def test_gcd_negative_a():
    response = client.get("/math/gcd?a=-1&b=5")
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "a and b must be non-negative"}}

def test_gcd_negative_b():
    response = client.get("/math/gcd?a=5&b=-1")
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "a and b must be non-negative"}}