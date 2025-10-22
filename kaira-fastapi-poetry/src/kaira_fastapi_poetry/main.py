# kaira_fastapi_poetry/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from kaira_fastapi_poetry.config import settings
from kaira_fastapi_poetry.api.endpoints import router as api_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Kaira 웹사이트를 서빙하는 FastAPI 서버",
)

# API 라우터 등록
app.include_router(api_router, prefix="/api", tags=["api"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Kaira Server!", "status": "ok"}


# 정적 파일 마운트
static_dir = Path(__file__).parent / settings.static_files_path
if static_dir.exists():
    app.mount(
        "/static", StaticFiles(directory=static_dir, html=True), name="static"
    )
else:
    print(f"⚠️  Warning: Static files not found at {static_dir}")
