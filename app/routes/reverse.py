from fastapi import APIRouter, HTTPException, Query
from typing import Optional

router = APIRouter()

@router.get("/strings/reverse")
def reverse(s: Optional[str] = Query(None)):
    if s is None:
        raise HTTPException(status_code=400, detail={"error": "s is required"})
    if len(s) > 1000:
        raise HTTPException(status_code=413, detail={"error": "too long"})
    return {"input": s, "reversed": s[::-1]}
