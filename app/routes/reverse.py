from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get("/text/reverse")
async def reverse_string(text: str = Query(..., description="Text to reverse")):
    if not text:
        raise HTTPException(status_code=400, detail={"error": "text parameter is required"})
    
    reversed_text = text[::-1]
    return {"original": text, "reversed": reversed_text}