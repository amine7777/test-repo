import math
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/math/factorial")
def factorial(n: int = Query(...)):
    if n < 0 or n > 20:
        raise HTTPException(status_code=400, detail={"error": "n must be 0-20"})
    return {"n": n, "result": math.factorial(n)}
