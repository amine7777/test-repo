import pytest
from fastapi.testclient import TestClient
from main import app, parse_response, call_llm
import json

client = TestClient(app)

class TestAnalyzeEndpoint:
    def test_analyze_endpoint_success(self):
        """Test the /analyze endpoint with valid input"""
        response = client.post("/analyze", json={"text": "This is a test message"})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "sentiment" in data
        assert "usefulness_score" in data
        assert "intent" in data
        assert isinstance(data["usefulness_score"], int)
        assert data["sentiment"] in ["positive", "neutral", "negative"]
        assert data["intent"] in ["informational", "decision", "brainstorm", "noise"]

    def test_analyze_endpoint_missing_text(self):
        """Test the /analyze endpoint with missing text field"""
        response = client.post("/analyze", json={})
        assert response.status_code == 422

    def test_analyze_endpoint_invalid_json(self):
        """Test the /analyze endpoint with invalid JSON"""
        response = client.post("/analyze", 
                             data="invalid json",
                             headers={"Content-Type": "application/json"})
        assert response.status_code == 422

class TestTestEndpoint:
    def test_test_endpoint_returns_results(self):
        """Test the /test endpoint returns expected structure"""
        response = client.get("/test")
        assert response.status_code == 200
        data = response.json()
        assert "executed" in data
        assert "results" in data
        assert data["executed"] == 4
        assert len(data["results"]) == 4
        
        # Check structure of results
        for result in data["results"]:
            assert "input" in result
            assert "output" in result
            assert isinstance(result["input"], str)
            assert "summary" in result["output"]
            assert "sentiment" in result["output"]
            assert "usefulness_score" in result["output"]
            assert "intent" in result["output"]

class TestHealthyEndpoint:
    def test_healthy_endpoint(self):
        """Test the /healthy endpoint returns OK status"""
        response = client.get("/healthy")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

class TestUtilityFunctions:
    def test_parse_response_valid_json(self):
        """Test parse_response with valid JSON"""
        valid_json = '{"summary": "Test", "sentiment": "positive", "usefulness_score": 80, "intent": "informational"}'
        result = parse_response(valid_json)
        assert result.summary == "Test"
        assert result.sentiment == "positive"
        assert result.usefulness_score == 80
        assert result.intent == "informational"

    def test_parse_response_invalid_json(self):
        """Test parse_response with invalid JSON falls back gracefully"""
        invalid_json = "not json"
        result = parse_response(invalid_json)
        assert result.summary == ""
        assert result.sentiment == "neutral"
        assert result.usefulness_score == 0
        assert result.intent == "noise"

    def test_parse_response_missing_fields(self):
        """Test parse_response with missing required fields"""
        incomplete_json = '{"summary": "Test"}'
        result = parse_response(incomplete_json)
        assert result.summary == ""
        assert result.sentiment == "neutral"
        assert result.usefulness_score == 0
        assert result.intent == "noise"

    def test_call_llm_fake_mode(self):
        """Test call_llm returns valid JSON in fake mode"""
        result = call_llm("test input")
        parsed = json.loads(result)
        assert "summary" in parsed
        assert "sentiment" in parsed
        assert "usefulness_score" in parsed
        assert "intent" in parsed
        assert parsed["sentiment"] in ["positive", "neutral", "negative"]
        assert parsed["intent"] in ["informational", "decision", "brainstorm", "noise"]
        assert isinstance(parsed["usefulness_score"], int)
        assert 0 <= parsed["usefullness_score"] <= 100

class TestIntegration:
    def test_full_workflow(self):
        """Integration test: full analyze workflow"""
        test_texts = [
            "I love this new feature!",
            "The system crashed unexpectedly",
            "What should we do next?",
            "Random noise here"
        ]
        
        for text in test_texts:
            response = client.post("/analyze", json={"text": text})
            assert response.status_code == 200
            data = response.json()
            
            # Verify all required fields are present and valid
            assert isinstance(data["summary"], str)
            assert data["sentiment"] in ["positive", "neutral", "negative"]
            assert isinstance(data["usefulness_score"], int)
            assert 0 <= data["usefullness_score"] <= 100
            assert data["intent"] in ["informational", "decision", "brainstorm", "noise"]

    def test_app_startup(self):
        """Test that the FastAPI app starts without errors"""
        response = client.get("/healthy")
        assert response.status_code == 200
