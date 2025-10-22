# app/main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

# 정적 파일 마운트
static_path = Path(__file__).parent.parent.parent/ "kaira-1.0.0"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/")
async def root():
    return {"message": "Kaira Static Server"}

