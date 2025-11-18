# syntax=docker/dockerfile:1

# === 1단계: Builder (의존성 설치) ===
FROM python:3.11-slim AS builder

WORKDIR /app

# 의존성 설치를 위해 requirements.txt 파일만 복사
COPY requirements.txt .

# 패키지들을 시스템 site-packages가 아닌 별도 디렉토리에 설치하여 복사를 용이하게 함
# --target 옵션을 사용하여 설치 위치를 지정
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --target=/app/packages -r requirements.txt


# === 2단계: Runtime (최소 이미지) ===
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # PYTHONPATH에 설치된 패키지 경로와 소스 코드 경로를 추가
    PYTHONPATH=/app/packages:/app/app \
    ENVIRONMENT=production

WORKDIR /app

# Builder에서 설치된 패키지들만 복사
COPY --from=builder /app/packages /app/packages

# PATH 환경 변수에 패키지 bin 디렉토리 추가
ENV PATH=/app/packages/bin:$PATH

# 앱 소스 코드 복사 (런타임 단계에서만 필요)
# kaira-server의 경우, 애플리케이션 코드가 'app' 디렉토리 안에 있다고 가정
COPY app ./app

# 비root 사용자로 실행 (보안 Best Practice)
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 포트 노출
EXPOSE 8000

# 앱 실행
# kaira-server의 실행 명령: uvicorn app.main:app --app-dir kaira-server
# Dockerfile 내에서는 WORKDIR이 /app이므로, app.main:app으로 바로 접근 가능
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
