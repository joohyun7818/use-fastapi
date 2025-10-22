# kaira_fastapi_poetry/api/endpoints.py
from fastapi import APIRouter

router = APIRouter()


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


@router.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}",
    }
