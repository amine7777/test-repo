from fastapi import FastAPI
from pydantic import BaseModel
import json
from typing import List, Dict, Any

# Mock LLM response for testing purposes
MOCK_LLM_RESPONSE = {
    "summary": "This is a mock summary.",
    "sentiment": "neutral",
    "usefulness_score": 75,
    "intent": "informational"
}

# --- Configuration ---
USE_FAKE_LLM = True  # Set to False to use a real LLM (requires API key setup)

# --- Pydantic Models ---
class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    summary: str
    sentiment: str
    usefulness_score: int
    intent: str

# --- Prompt Engineering ---
PROMPT_TEMPLATE = """
Analyze the following text and return a JSON object with the specified fields.

Constraints:
- Output MUST be a valid JSON object.
- Do not include any explanations or introductory text outside the JSON.

Fields:
- summary: A concise summary of the text (maximum 20 words).
- sentiment: The overall sentiment of the text. Must be one of: "positive", "neutral", "negative".
- usefulness_score: An integer score between 0 and 100 indicating how useful the text is.
- intent: The primary intent of the text. Must be one of: "informational", "decision", "brainstorm", "noise".

Scoring Rules for usefulness_score and intent:
- usefulness_score: Higher scores for text that is clear, actionable, or informative. Lower scores for vague, repetitive, or irrelevant text.
- intent:
    - informational: Text primarily aims to convey facts or knowledge.
    - decision: Text aims to help make a choice or judgment.
    - brainstorm: Text aims to generate ideas or explore possibilities.
    - noise: Text is irrelevant, spam, or lacks clear purpose.

Text to analyze:
{text}

JSON Output:
"""

# --- LLM Layer ---
def call_llm(text: str) -> str:
    """Calls the LLM to get the analysis. Returns raw JSON string."""
    if USE_FAKE_LLM:
        print("Using fake LLM response.")
        return json.dumps(MOCK_LLM_RESPONSE)
    else:
        # In a real scenario, you would use an LLM client here (e.g., OpenAI)
        # Example using a hypothetical client:
        # import openai
        # openai.api_key = "YOUR_API_KEY"
        # prompt = PROMPT_TEMPLATE.format(text=text)
        # response = openai.Completion.create(
        #     model="text-davinci-003", # or another suitable model
        #     prompt=prompt,
        #     temperature=0,
        #     max_tokens=150
        # )
        # return response.choices[0].text.strip()
        print("Real LLM call not implemented. Returning mock response.")
        return json.dumps(MOCK_LLM_RESPONSE)

# --- Parsing & Safety ---
def parse_llm_output(raw_output: str) -> AnalysisResponse:
    """Safely parses and validates LLM output."""
    default_response = AnalysisResponse(
        summary="Analysis failed. Could not parse output.",
        sentiment="neutral",
        usefulness_score=0,
        intent="noise"
    )
    try:
        data = json.loads(raw_output)
        # Validate with Pydantic model
        return AnalysisResponse(**data)
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        print(f"JSON parsing or Pydantic validation failed: {e}")
        return default_response
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        return default_response

# --- FastAPI App ---
app = FastAPI()

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_text(request: AnalysisRequest):
    """Analyzes the input text using the LLM."""
    raw_llm_output = call_llm(request.text)
    return parse_llm_output(raw_llm_output)

@app.get("/test")
def run_tests() -> Dict[str, Any]:
    """Runs predefined test cases against the /analyze endpoint logic."""
    test_cases = [
        {
            "name": "Positive Sentiment Example",
            "input_text": "This is a fantastic product! I love it. Highly recommend.",
            "expected_sentiment": "positive"
        },
        {
            "name": "Neutral Sentiment Example",
            "input_text": "The weather today is partly cloudy with a chance of rain later.",
            "expected_sentiment": "neutral"
        },
        {
            "name": "Negative Sentiment Example",
            "input_text": "I am very disappointed with the service. It was slow and unhelpful.",
            "expected_sentiment": "negative"
        },
        {
            "name": "Brainstorm Intent Example",
            "input_text": "What are some creative ways to market a new app? Let's brainstorm ideas.",
            "expected_intent": "brainstorm"
        }
    ]

    results = []
    for i, case in enumerate(test_cases):
        input_text = case["input_text"]
        # Simulate calling the core analysis logic directly
        raw_output = call_llm(input_text)
        parsed_output = parse_llm_output(raw_output)

        # Basic assertion for demonstration; a real test suite would be more robust
        sentiment_match = parsed_output.sentiment == case.get("expected_sentiment")
        intent_match = parsed_output.intent == case.get("expected_intent")
        usefulness_score_valid = 0 <= parsed_output.usefulness_score <= 100

        results.append({
            "test_case_name": case["name"],
            "input": input_text,
            "output": parsed_output.dict(),
            "assertions": {
                "sentiment_correct": sentiment_match if "expected_sentiment" in case else None,
                "intent_correct": intent_match if "expected_intent" in case else None,
                "usefulness_score_valid": usefulness_score_valid
            }
        })

    return {
        "total_tests_executed": len(test_cases),
        "test_results": results
    }

@app.get("/hello")
def hello_world():
    return {"message": "hello world :)"}

# --- Run Instructions ---
# To run this application:
# 1. Save the code as main.py
# 2. Install dependencies: pip install fastapi uvicorn pydantic
# 3. Run the server: uvicorn main:app --reload
