from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="Kaira Server",
    version="0.1.0",
    description="kaira 웹사이트를 서빙하는 FastAPI 서버"
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    '''헬스 체크 엔드포인트'''
    return {"message": "Welcome to kaira Server!", "status": "ok"}

@app.get("/api/info")
def get_info():
    '''서버정보'''
    return {
        "name": "Kaira Server",
        "version": "0.1.0",
        "description": "정적 웹사이트 서빙 서버"
    }

@app.get("/api/items/{item_id}")
def get_item(item_id:int):
    '''ID로 아이템 조회'''
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}"
    }


#정적 파일 마운트
static_dir = Path(__file__).parent.parent / "kaira-1.0.0"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")


