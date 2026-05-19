from fastapi import APIRouter, HTTPException, Query
import math

router = APIRouter()

@router.get("/math/factorial")
async def get_factorial(n: int = Query(..., description="Number to calculate factorial for")):
    if n < 0 or n > 20:
        raise HTTPException(status_code=400, detail={"error": "n must be 0-20"})
    
    result = math.factorial(n)
    return {"n": n, "result": result}