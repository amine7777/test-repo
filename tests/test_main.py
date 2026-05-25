import pytest
from fastapi.testclient import TestClient
import json
import os

# Import the app and utility functions
from main import app, call_llm, parse_response, AnalyzeResponse

client = TestClient(app)

class TestAnalyzeEndpoint:
    """Test the main /analyze POST endpoint"""
    
    def test_analyze_success(self):
        """Test successful text analysis"""
        response = client.post("/analyze", json={"text": "I love sunny days"})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "sentiment" in data
        assert "usefulness_score" in data
        assert "intent" in data
        assert data["sentiment"] in ["positive", "neutral", "negative"]
        assert data["intent"] in ["informational", "decision", "brainstorm", "noise"]
        assert isinstance(data["usefulness_score"], int)
        assert 0 <= data["usefulness_score"] <= 100

    def test_analyze_empty_text(self):
        """Test analysis with empty text"""
        response = client.post("/analyze", json={"text": ""})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert "sentiment" in data
        assert "usefulness_score" in data
        assert "intent" in data

    def test_analyze_invalid_request(self):
        """Test analysis with invalid request body"""
        response = client.post("/analyze", json={"wrong_field": "test"})
        assert response.status_code == 422  # Validation error

class TestTestEndpoint:
    """Test the /test GET endpoint"""
    
    def test_run_tests(self):
        """Test the test runner endpoint"""
        response = client.get("/test")
        assert response.status_code == 200
        data = response.json()
        assert "executed" in data
        assert "results" in data
        assert isinstance(data["executed"], int)
        assert data["executed"] == 4  # Should run 4 test cases
        assert len(data["results"]) == 4
        
        # Verify each result has proper structure
        for result in data["results"]:
            assert "input" in result
            assert "output" in result
            output = result["output"]
            assert "summary" in output
            assert "sentiment" in output
            assert "usefulness_score" in output
            assert "intent" in output

class TestHealthyEndpoint:
    """Test the /healthy GET endpoint"""
    
    def test_healthy(self):
        """Test health check endpoint"""
        response = client.get("/healthy")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

class TestUtilityFunctions:
    """Test utility functions directly"""
    
    def test_call_llm_fake_mode(self):
        """Test call_llm in fake mode"""
        os.environ["USE_FAKE_LLM"] = "true"
        result = call_llm("test text")
        assert isinstance(result, str)
        parsed = json.loads(result)
        assert "summary" in parsed
        assert "sentiment" in parsed
        assert "usefulness_score" in parsed
        assert "intent" in parsed

    def test_parse_response_valid_json(self):
        """Test parsing valid JSON response"""
        valid_json = json.dumps({
            "summary": "Test summary",
            "sentiment": "positive",
            "usefulness_score": 85,
            "intent": "informational"
        })
        result = parse_response(valid_json)
        assert isinstance(result, AnalyzeResponse)
        assert result.summary == "Test summary"
        assert result.sentiment == "positive"
        assert result.usefulness_score == 85
        assert result.intent == "informational"

    def test_parse_response_invalid_json(self):
        """Test parsing invalid JSON falls back to default"""
        invalid_json = "not valid json"
        result = parse_response(invalid_json)
        assert isinstance(result, AnalyzeResponse)
        assert result.summary == ""
        assert result.sentiment == "neutral"
        assert result.usefulness_score == 0
        assert result.intent == "noise"

    def test_parse_response_missing_fields(self):
        """Test parsing JSON with missing required fields"""
        incomplete_json = json.dumps({"summary": "Only summary"})
        result = parse_response(incomplete_json)
        assert isinstance(result, AnalyzeResponse)
        assert result.summary == ""
        assert result.sentiment == "neutral"
        assert result.usefulness_score == 0
        assert result.intent == "noise"

class TestIntegration:
    """Integration tests for full workflows"""
    
    def test_full_workflow_fake_llm(self):
        """Test complete workflow with fake LLM"""
        os.environ["USE_FAKE_LLM"] = "true"
        
        # Test analyze endpoint
        response = client.post("/analyze", json={"text": "This is a test sentence"})
        assert response.status_code == 200
        
        # Test health check
        health_response = client.get("/healthy")
        assert health_response.status_code == 200
        
        # Test runner
        test_response = client.get("/test")
        assert test_response.status_code == 200

    def test_multiple_analyze_calls(self):
        """Test multiple calls to analyze endpoint"""
        test_texts = [
            "I am very happy today",
            "The weather is okay", 
            "This is terrible news",
            ""
        ]
        
        for text in test_texts:
            response = client.post("/analyze", json={"text": text})
            assert response.status_code == 200
            data = response.json()
            assert all(key in data for key in ["summary", "sentiment", "usefulness_score", "intent"])
