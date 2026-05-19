import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_reverse_basic():
    response = client.get("/text/reverse?text=hello")
    assert response.status_code == 200
    assert response.json() == {"original": "hello", "reversed": "olleh"}

def test_reverse_single_char():
    response = client.get("/text/reverse?text=a")
    assert response.status_code == 200
    assert response.json() == {"original": "a", "reversed": "a"}

def test_reverse_palindrome():
    response = client.get("/text/reverse?text=racecar")
    assert response.status_code == 200
    assert response.json() == {"original": "racecar", "reversed": "racecar"}

def test_reverse_with_spaces():
    response = client.get("/text/reverse?text=hello world")
    assert response.status_code == 200
    assert response.json() == {"original": "hello world", "reversed": "dlrow olleh"}

def test_reverse_empty():
    response = client.get("/text/reverse?text=")
    assert response.status_code == 400
    assert response.json() == {"detail": {"error": "text parameter is required"}}