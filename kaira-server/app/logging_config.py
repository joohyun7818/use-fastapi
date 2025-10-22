# app/logging_config.py
import logging
import sys
from pathlib import Path

def setup_logging():
    """로깅 설정"""
    # 로그 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
  
    # 로그 포맷 설정
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
  
    # 루트 로거 설정
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            # 콘솔 출력
            logging.StreamHandler(sys.stdout),
            # 파일 출력
            logging.FileHandler(log_dir / "app.log", encoding="utf-8")
        ]
    )
  
    # 특정 로거 레벨 조정
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)

# 로거 생성 함수
def get_logger(name: str):
    """로거 인스턴스 생성"""
    return logging.getLogger(name)