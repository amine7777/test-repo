from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/analyze", json={"text": "Sample text for analysis."})
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {"summary", "sentiment", "usefulness_score", "intent"}
    assert isinstance(data["summary"], str)
    assert data["sentiment"] in {"positive", "neutral", "negative"}
    assert isinstance(data["usefulness_score"], int)
    assert data["intent"] in {"informational", "decision", "brainstorm", "noise"}

def test_test_endpoint():
    response = client.get("/test")
    assert response.status_code == 200
    data = response.json()
    assert data["executed"] == 4
    assert isinstance(data["results"], list)
    assert len(data["results"]) == 4
    for item in data["results"]:
        assert "input" in item and "output" in item
        out = item["output"]
        assert set(out.keys()) == {"summary", "sentiment", "usefulness_score", "intent"}
