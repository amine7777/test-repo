import math
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/math/gcd")
def gcd(a: int = Query(...), b: int = Query(...)):
    if a < 0 or b < 0:
        raise HTTPException(status_code=400, detail={"error": "a and b must be non-negative"})
    return {"a": a, "b": b, "gcd": math.gcd(a, b)}
