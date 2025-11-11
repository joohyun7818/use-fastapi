# kaira_fastapi_poetry/api/endpoints.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from kaira_fastapi_poetry.logging_config import get_logger
from kaira_fastapi_poetry.config import settings

router = APIRouter()
logger = get_logger(__name__)


# Pydantic 스키마
class CreateItem(BaseModel):
    """아이템 생성 모델"""
    name: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)

# 샘플 데이터베이스
items_db = {"item1": "book", "item2": "pen", "item3": "notebook"}


@router.get("/health")
def health_check():
    return {"status": "healthy", "service": "kaira-server"}


@router.get("/info")
def get_info():
    return {
        "name": "Kaira Server",
        "version": "0.1.0",
        "description": "정적 웹사이트 서빙 서버",
    }


@router.get("/")
async def root():
    logger.info("루트 엔드포인트에 접근했습니다.")
    return {
        "app": settings.app_name,
        "environment": settings.environment
    }


@router.get("/config")
async def get_config():
    if not settings.debug:
        return {"error": "Config access is only available in debug mode."}
    return {
        "app_name": settings.app_name,
        "environment": settings.environment,
        "static_dir": str(settings.static_path),
        "log_level": settings.log_level,
    }


@router.get("/items/{item_id}")
async def get_item(item_id: str):
    logger.info(f"Item 요청: {item_id}")
    if item_id not in items_db:
        logger.info(f"Item {item_id} not found.")
        raise HTTPException(
            status_code=404, 
            detail=f"Item {item_id} not found"
        )
    logger.debug(f"Item {item_id} found: {items_db[item_id]}")
    return {"item_id": item_id, "name": items_db[item_id]}


@router.get("/items-header/{item_id}")
async def get_item_with_header(item_id: str):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404, 
            detail="Item not found",
            headers={"X-Error": "Custom error header"}
        )
    return {"item_id": item_id, "name": items_db[item_id]}


@router.post("/validated-items/")
async def create_validated_item(item: CreateItem):
    return {"item": item}
