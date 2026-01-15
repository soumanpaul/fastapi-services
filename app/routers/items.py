from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
def list_items():
    return {"items": ["item1", "item2", "item3"]}
