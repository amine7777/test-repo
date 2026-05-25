from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
import json
import os
import math

app = FastAPI()

USE_FAKE_LLM = os.getenv("USE_FAKE_LLM", "true").lower() == "true"

PROMPT_TEMPLATE = """You are an AI that analyses text and returns a JSON object with the following fields:\n- summary: a concise summary (max 20 words)\n- sentiment: one of 'positive', 'neutral', 'negative'\n- usefulness_score: integer 0-100 indicating how useful the text is\n- intent: one of 'informational', 'decision', 'brainstorm', 'noise'\nEnsure the output is valid JSON and nothing else. Use temperature=0."""

FACTORIAL_MAX_N = 1000

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    summary: str
    sentiment: str
    usefulness_score: int
    intent: str

def call_llm(text: str) -> str:
    if USE_FAKE_LLM:
        return json.dumps({
            "summary": "Mock summary",
            "sentiment": "neutral",
            "usefulness_score": 50,
            "intent": "informational"
        })
    raise NotImplementedError("Real LLM integration not implemented")

def parse_response(raw: str) -> AnalyzeResponse:
    try:
        data = json.loads(raw)
        return AnalyzeResponse(**data)
    except (json.JSONDecodeError, ValidationError, TypeError):
        return AnalyzeResponse(summary="", sentiment="neutral", usefulness_score=0, intent="noise")

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    raw = call_llm(req.text)
    return parse_response(raw)

@app.get("/test")
async def run_tests():
    test_cases = ["I love sunny days.", "The server crashed unexpectedly.", "What is the meaning of life?", "Buy milk and eggs."]
    results = []
    for case in test_cases:
        raw = call_llm(case)
        resp = parse_response(raw)
        results.append({"input": case, "output": resp.dict()})
    return {"executed": len(test_cases), "results": results}

@app.get("/healthy")
async def healthy():
    return {"status": "ok"}

@app.get("/factorial")
async def factorial(n: int):
    if n < 0:
        raise HTTPException(status_code=400, detail="n must be a non-negative integer")
    if n > FACTORIAL_MAX_N:
        raise HTTPException(status_code=400, detail=f"n must be <= {FACTORIAL_MAX_N}")
    return {"result": math.factorial(n)}
