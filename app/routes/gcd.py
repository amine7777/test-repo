from fastapi import APIRouter, HTTPException, Query
import math

router = APIRouter()

@router.get("/math/gcd")
async def get_gcd(a: int = Query(..., description="First number"), 
                  b: int = Query(..., description="Second number")):
    if a < 0 or b < 0:
        raise HTTPException(status_code=400, detail={"error": "a and b must be non-negative"})
    
    result = math.gcd(a, b)
    return {"a": a, "b": b, "gcd": result}