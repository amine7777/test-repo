from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
import json

app = FastAPI()

PROMPT_TEMPLATE = """
Analyze the following text and return ONLY a valid JSON object.

Rules:
1. summary: max 20 words.
2. sentiment: 'positive', 'neutral', or 'negative'.
3. usefulness_score: integer 0-100.
4. intent: 'informational', 'decision', 'brainstorm', or 'noise'.

Text: {text}
"""

USE_FAKE_LLM = True

class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    summary: str
    sentiment: Literal["positive", "neutral", "negative"]
    usefulness_score: int = Field(ge=0, le=100)
    intent: Literal["informational", "decision", "brainstorm", "noise"]

def call_llm(text: str) -> str:
    if USE_FAKE_LLM:
        return json.dumps({
            "summary": "This is a mock summary of the provided text.",
            "sentiment": "neutral",
            "usefulness_score": 50,
            "intent": "informational"
        })
    # Real LLM implementation would go here
    return "{}"

def parse_analysis(raw_json: str) -> AnalysisResponse:
    try:
        data = json.loads(raw_json)
        return AnalysisResponse(**data)
    except Exception:
        return AnalysisResponse(
            summary="Error parsing analysis.",
            sentiment="neutral",
            usefulness_score=0,
            intent="noise"
        )

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze(request: AnalysisRequest) -> AnalysisResponse:
    raw_output = call_llm(request.text)
    return parse_analysis(raw_output)

@app.get("/seb", response_model=AnalysisResponse)
async def seb(text: str = "Default text for seb endpoint") -> AnalysisResponse:
    """Endpoint requested in issue #9"""
    return await analyze(AnalysisRequest(text=text))

@app.get("/test")
async def test_suite():
    test_cases = [
        "I love this product!",
        "How do I reset my password?",
        "The weather is okay.",
        "Random gibberish 12345"
    ]
    results = []
    for tc in test_cases:
        res = await analyze(AnalysisRequest(text=tc))
        results.append({"input": tc, "output": res.dict()})
    
    return {
        "tests_executed": len(test_cases),
        "results": results
    }

@app.get("/healthy")
async def healthy():
    return {"status": "healthy"}

# Run Instructions:
# pip install fastapi uvicorn
# uvicorn main:app --reload