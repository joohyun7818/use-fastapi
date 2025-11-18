# syntax=docker/dockerfile:1

# === 1단계: Builder (의존성 설치) ===
FROM python:3.11-slim AS builder

# Poetry 설치
RUN pip install --no-cache-dir poetry==1.8.5

WORKDIR /app

# Poetry 설정: 가상환경 생성 안 함
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

# 의존성 파일 복사 및 설치 (캐싱 최적화)
COPY pyproject.toml poetry.lock ./

# 소스 코드 복사 (poetry install이 packages를 찾기 위해 필요)
COPY ./src ./src

RUN poetry install --no-root --only main

# === 2단계: Runtime (최소 이미지) ===
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    ENVIRONMENT=production

WORKDIR /app

# Builder에서 설치된 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 앱 코드 복사
COPY ./src ./src

# 비root 사용자로 실행 (보안 Best Practice)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 포트 노출
EXPOSE 8000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 앱 실행
CMD ["uvicorn", "kaira_fastapi_poetry.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

