from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import json
from typing import List, Dict, Any

# --- Configuration ---
USE_FAKE_LLM = os.environ.get("USE_FAKE_LLM", "false").lower() == "true"

# --- Pydantic Models ---
class AnalysisRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    summary: str = Field(..., max_length=20)
    sentiment: str
    usefulness_score: int = Field(..., ge=0, le=100)
    intent: str

class TestResult(BaseModel):
    input_text: str
    expected_output: Dict[str, Any]
    actual_output: Dict[str, Any]
    passed: bool

class TestSummary(BaseModel):
    total_tests: int
    passed_tests: int
    results: List[TestResult]

# --- Prompt Engineering ---
PROMPT_TEMPLATE = """Analyze the following text and return a JSON object with the specified fields.

Output JSON structure:
{{
  "summary": "A concise summary of the text (maximum 20 words).",
  "sentiment": "The overall sentiment of the text ('positive', 'neutral', or 'negative').",
  "usefulness_score": "A score from 0 to 100 indicating how useful the text is.",
  "intent": "The primary intent of the text ('informational', 'decision', 'brainstorm', or 'noise')."
}}

Scoring Rules:
- Summary: Be brief and capture the main point.
- Sentiment: Positive if expressing favorable opinions, Negative if unfavorable, Neutral otherwise.
- Usefulness Score: High for actionable or informative content, low for trivial or irrelevant content.
- Intent: Informational if providing facts, Decision if prompting a choice, Brainstorm if generating ideas, Noise if irrelevant or spam.

Constraints:
- The output MUST be a valid JSON object ONLY. Do not include any other text before or after the JSON.
- All fields must be present and adhere to their types and constraints.

Text to analyze: {text}

JSON Output: """

# --- LLM Layer ---
def call_llm(text: str) -> str:
    prompt = PROMPT_TEMPLATE.format(text=text)
    if USE_FAKE_LLM:
        # Mock response for testing/development
        return json.dumps({
            "summary": "This is a fake summary.",
            "sentiment": "neutral",
            "usefulness_score": 50,
            "intent": "informational"
        })
    else:
        # In a real application, you would use an LLM client here (e.g., OpenAI)
        # For this example, we'll simulate a call and raise an error if not mocked
        # Replace with actual LLM API call
        # Example using OpenAI:
        # import openai
        # openai.api_key = os.environ.get("OPENAI_API_KEY")
        # response = openai.Completion.create(
        #     model="text-davinci-003",
        #     prompt=prompt,
        #     temperature=0,
        #     max_tokens=150
        # )
        # return response.choices[0].text.strip()
        raise NotImplementedError("Real LLM call not implemented. Set USE_FAKE_LLM=true or implement the LLM client.")

# --- Parsing & Safety ---
def parse_and_validate_llm_output(llm_output: str) -> Dict[str, Any]:
    default_response = {
        "summary": "Analysis failed.",
        "sentiment": "neutral",
        "usefulness_score": 0,
        "intent": "noise"
    }
    try:
        data = json.loads(llm_output)
        # Validate against Pydantic model
        validated_data = AnalysisResponse(**data)
        return validated_data.dict()
    except (json.JSONDecodeError, pydantic.ValidationError):
        return default_response

# --- FastAPI App ---
app = FastAPI()

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_text(request: AnalysisRequest):
    try:
        llm_response_str = call_llm(request.text)
        parsed_response = parse_and_validate_llm_output(llm_response_str)
        return AnalysisResponse(**parsed_response)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/test", response_model=TestSummary)
def run_tests():
    test_cases = [
        {
            "input_text": "This is a fantastic product! I highly recommend it. It works perfectly.",
            "expected_output": {
                "summary": "Fantastic product, highly recommended, works perfectly.",
                "sentiment": "positive",
                "usefulness_score": 90,
                "intent": "decision"
            }
        },
        {
            "input_text": "The weather today is partly cloudy with a chance of rain later.",
            "expected_output": {
                "summary": "Partly cloudy today with a chance of rain.",
                "sentiment": "neutral",
                "usefulness_score": 70,
                "intent": "informational"
            }
        },
        {
            "input_text": "I'm not sure what to do next. Maybe we can brainstorm some ideas?",
            "expected_output": {
                "summary": "Unsure about next steps, suggests brainstorming ideas.",
                "sentiment": "neutral",
                "usefulness_score": 60,
                "intent": "brainstorm"
            }
        },
        {
            "input_text": "asdfjkl; qweruiop zxcvbnm",
            "expected_output": {
                "summary": "Analysis failed.",
                "sentiment": "neutral",
                "usefulness_score": 0,
                "intent": "noise"
            }
        }
    ]

    results = []
    passed_count = 0

    # Temporarily set USE_FAKE_LLM to true for predictable test results
    global USE_FAKE_LLM
    original_use_fake_llm = USE_FAKE_LLM
    USE_FAKE_LLM = True

    for case in test_cases:
        try:
            # Call the analyze logic directly for testing purposes
            # In a real scenario, you might use TestClient to call the endpoint
            mock_llm_response = call_llm(case["input_text"])
            actual_output = parse_and_validate_llm_output(mock_llm_response)
            
            # Basic check: compare sentiment and intent for simplicity
            # A more robust test would compare all fields or use fuzzy matching
            passed = (
                actual_output["sentiment"] == case["expected_output"].get("sentiment", "neutral") and
                actual_output["intent"] == case["expected_output"].get("intent", "noise")
            )
            if passed:
                passed_count += 1

            results.append(TestResult(
                input_text=case["input_text"],
                expected_output=case["expected_output"],
                actual_output=actual_output,
                passed=passed
            ))
        except Exception as e:
            results.append(TestResult(
                input_text=case["input_text"],
                expected_output=case["expected_output"],
                actual_output={"error": str(e)},
                passed=False
            ))

    # Restore original USE_FAKE_LLM setting
    USE_FAKE_LLM = original_use_fake_llm

    return TestSummary(
        total_tests=len(test_cases),
        passed_tests=passed_count,
        results=results
    )

# --- Run Instructions ---
# To run this application:
# 1. Install dependencies:
#    pip install fastapi uvicorn pydantic
#
# 2. Run the server:
#    uvicorn main:app --reload
#
# 3. Test the API:
#    curl -X POST "http://127.0.0.1:8000/analyze" -H "Content-Type: application/json" -d '{"text": "Your text here"}'
#    curl http://127.0.0.1:8000/test
