# kaira_fastapi_poetry/middleware/logging.py
import time
import logging
from fastapi import Request

logger = logging.getLogger(__name__)

async def log_requests(request: Request, call_next):
    """요청/응답 로깅 미들웨어"""
    # 요청 시작 시간
    start_time = time.time()
  
    # 요청 정보 로깅
    logger.info(f"요청 시작: {request.method} {request.url.path}")
    logger.debug(f"요청 헤더: {dict(request.headers)}")
  
    # 요청 처리
    response = await call_next(request)
  
    # 처리 시간 계산
    process_time = time.time() - start_time
  
    # 응답 정보 로깅
    logger.info(
        f"요청 완료: {request.method} {request.url.path} "
        f"- 상태: {response.status_code} - 시간: {process_time:.3f}초"
    )
  
    # 응답 헤더에 처리 시간 추가
    response.headers["X-Process-Time"] = str(process_time)
  
    return response
