# app/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pathlib import Path
from contextlib import asynccontextmanager
from app.logging_config import setup_logging, get_logger

class ItemNotFoundException(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id


setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    logger.info("애플리케이션이 시작되었습니다.")
    yield
    # shutdown (필요시 추가)


app = FastAPI(lifespan=lifespan)


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


# 기본 제공되는 에러 핸들러 오버라이딩
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """검증 에러 커스터마이징"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
  
    return JSONResponse(
        status_code=422,
        content={
            "error": "ValidationError",
            "message": "입력 데이터가 올바르지 않습니다",
            "details": errors
        }
    )

from pydantic import BaseModel

class CreateItem(BaseModel):
    name: str
    price: float

@app.post("/validated-items/")
async def create_validated_item(item: CreateItem):
    return {"item": item}