import os
import json
from fastapi.testclient import TestClient

# Ensure the application uses the mock LLM during tests
os.environ.setdefault("USE_MOCK_LLM", "true")

from main import app

client = TestClient(app)


def test_analyze_typical():
    payload = {"text": "The quick brown fox jumps over the lazy dog."}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "summary" in data
    assert isinstance(data["summary"], str)


def test_analyze_empty_text():
    payload = {"text": ""}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data.get("summary") == ""


def test_analyze_missing_field():
    response = client.post("/analyze", json={})
    assert response.status_code == 422  # FastAPI validation error for missing required field


def test_analyze_non_string():
    payload = {"text": 12345}
    response = client.post("/analyze", json=payload)
    assert response.status_code == 422  # Validation should reject non‑string input