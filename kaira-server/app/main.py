# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pathlib import Path

class ItemNotFoundException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id

app = FastAPI()
items_db = {"item1": "book", "item2": "pen", "item3": "notebook"}

# 정적 파일 마운트
static_path = Path(__file__).parent.parent.parent/ "kaira-1.0.0"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def root():
    return {"message": "Kaira Static Server"}

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404, 
            detail=f"Item {item_id} not found"
        )
    return {"item_id": item_id, "name": items_db[item_id]}

@app.get("/items-header/{item_id}")
async def get_item_with_header(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404, 
            detail="Item not found",
            headers={"X-Error": "Custom error header"}
        )
    return {"item_id": item_id, "name": items_db[item_id]}

# 커스텀 예외 핸들러
@app.exception_handler(ItemNotFoundException)
async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    '''커스텀 예외 핸들러'''
    return JSONResponse(
        status_code=404,
        content={
            "error": "ItemNotFound",
            "message": f"Item {exc.item_id} not found.",
            "suggestion": "Please check the item ID and try again."
        },
    )

@app.get("/custom-items/{item_id}")
async def get_custom_item(item_id: str):
    if item_id not in items_db:
        raise ItemNotFoundException(item_id=item_id)
    return {"item_id": item_id, "name": items_db[item_id]}