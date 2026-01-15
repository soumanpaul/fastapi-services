from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
import asyncio
from app.routers import items

app = FastAPI()

FAKE_DB = {1: {"name": "Book"}}

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True    

@app.get('/')
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    if item_id not in FAKE_DB:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return FAKE_DB[item_id]

@app.post("/items", status_code=status.HTTP_201_CREATED)
def add_item():
    return {"ok": True}

# 6) Async endpoints (when you do I/O)
# Use async def when you call async libraries (http/db).
@app.get("/ping")
async def ping():
    await asyncio.sleep(0.1)
    return {"pong": True}

# 7) Dependency Injection (superpower)
# Common use: auth, db sessions, shared logic.

def get_token():
    return "secrettoken"

@app.get('/secure')
def secure(token: str = Depends(get_token)):
    if token != "secrettoken":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    return {"secure_data": "This is secure"}

app.include_router(items.router)
