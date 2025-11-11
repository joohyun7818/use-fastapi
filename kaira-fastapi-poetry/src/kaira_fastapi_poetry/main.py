# kaira_fastapi_poetry/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path
from contextlib import asynccontextmanager

from kaira_fastapi_poetry.logging_config import setup_logging, get_logger
from kaira_fastapi_poetry.middleware.logging import log_requests
from kaira_fastapi_poetry.config import settings
from kaira_fastapi_poetry.database import Base, engine
from kaira_fastapi_poetry.api.endpoints import router as api_router
from kaira_fastapi_poetry.api.users import router as users_router
from kaira_fastapi_poetry.api.posts import router as posts_router


# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)


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
    # shutdown 
    logger.info("애플리케이션이 종료됩니다.")


app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
    version=settings.app_version,
    description="Kaira 웹사이트를 서빙하는 FastAPI 서버",
    debug=settings.debug,
)

# 미들웨어 등록
app.middleware("http")(log_requests)

# 데이터베이스 기반 API 라우터 등록
app.include_router(users_router)
app.include_router(posts_router)

# 기존 API 라우터 등록 (호환성 유지)
app.include_router(api_router, prefix="/api", tags=["api"])

# 루트 경로에서 HTML 반환 - /으로 접근시 HTML 페이지 반환
@app.get("/")
async def get_main_page():
    """HTML 메인 페이지 반환"""
    logger.info("/main 경로 접근 - index.html 반환")
    html_path = settings.static_path / "index.html"
    
    if not html_path.exists():
        logger.error(f"index.html을 찾을 수 없습니다: {html_path}")
        raise HTTPException(status_code=404, detail="index.html not found")
    
    return FileResponse(html_path)

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


# custom-items 엔드포인트 (커스텀 예외 테스트용)
items_db = {"item1": "book", "item2": "pen", "item3": "notebook"}


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


# 정적 파일 마운트
if settings.static_path.exists():
    logger.info(f"정적 파일 디렉토리 마운트: {settings.static_path}")
    # 루트 경로에 정적 파일 마운트 (html=True로 SPA 지원)
    app.mount("/",
              StaticFiles(directory=str(settings.static_path), html=True), 
                name="static")
else:
    logger.info("정적 파일 디렉토리를 찾을 수 없습니다.")
    static_path = Path(__file__).parent / settings.static_files_path
    if static_path.exists():
        logger.info(f"대체 경로에서 정적 파일 마운트: {static_path}")
        app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
    else:
        logger.warning(f"⚠️  Warning: Static files not found at {static_path}")

