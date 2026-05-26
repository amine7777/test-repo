from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/analyze", json={"text": "Test input"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert set(data.keys()) == {"summary", "sentiment", "usefulness_score", "intent"}

def test_test_endpoint():
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert data["executed"] == 4
    assert isinstance(data["results"], list)
    for item in data["results"]:
        assert "input" in item and "output" in item
        out = item["output"]
        assert set(out.keys()) == {"summary", "sentiment", "usefulness_score", "intent"}
