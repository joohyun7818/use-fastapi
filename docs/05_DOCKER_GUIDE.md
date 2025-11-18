# 05. Docker 컨테이너화 완벽 가이드

> FastAPI 애플리케이션을 Docker로 컨테이너화하고 docker-compose로 관리하는 방법을 배웁니다.

## 📚 5단계 목차

| 챕터                            | 주제                    | 예상 시간 |
| ------------------------------- | ----------------------- | --------- |
| [5.1](#51-docker-개념-이해)        | Docker 개념 이해        | 30분      |
| [5.2](#52-dockerfile-작성)         | Dockerfile 작성         | 1시간     |
| [5.3](#53-이미지-빌드와-실행)      | 이미지 빌드와 실행      | 45분      |
| [5.4](#54-docker-compose-활용)     | docker-compose 활용     | 1시간     |
| [5.5](#55-최적화와-best-practices) | 최적화와 Best Practices | 1시간     |
| [5.6](#56-로컬-개발-환경-구성)     | 로컬 개발 환경 구성     | 1시간     |
| [5.7](#57-프로덕션-배포-준비)      | 프로덕션 배포 준비      | 1시간     |
| [5.8](#58-문제-해결)               | 문제 해결               | 30분      |
| [5.9](#59-체크리스트)              | 체크리스트              | -         |

---

## 5.1 Docker 개념 이해

### 5.1.1 Docker란?

Docker는 애플리케이션을 **컨테이너**라는 표준화된 단위로 패키징하고 실행하는 플랫폼입니다.

**핵심 개념**:

- **이미지(Image)**: 애플리케이션 실행에 필요한 모든 것(코드, 라이브러리, 설정)이 담긴 템플릿
- **컨테이너(Container)**: 이미지를 실행한 인스턴스
- **Dockerfile**: 이미지를 만드는 레시피
- **Registry**: 이미지를 저장하는 저장소 (Docker Hub 등)

### 5.2.2 왜 Docker를 사용하는가?

**문제점 (Docker 없이)**:

```
개발자: "내 컴퓨터에서는 잘 되는데요..."
운영자: "서버에서는 안 돌아가요..."
```

**해결책 (Docker 사용)**:

- ✅ **일관성**: 어디서든 같은 환경
- ✅ **격리성**: 각 앱이 독립적으로 실행
- ✅ **이식성**: 어떤 서버에도 쉽게 배포
- ✅ **효율성**: 가상머신보다 가볍고 빠름

### 5.2.3 Docker 설치

**macOS**:

```bash
# Docker Desktop 다운로드 및 설치
# https://docs.docker.com/desktop/install/mac-install/

# 설치 확인
docker --version
docker compose version
```

**Ubuntu/Linux**:

```bash
# Docker Engine 설치
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 설치 확인
docker --version
docker compose version

# 현재 사용자를 docker 그룹에 추가 (sudo 없이 사용)
sudo usermod -aG docker $USER
newgrp docker
```

**Windows**:

```powershell
# Docker Desktop 다운로드 및 설치
# https://docs.docker.com/desktop/install/windows-install/

# PowerShell에서 확인
docker --version
docker compose version
```

### 5.2.4 Docker 기본 명령어

```bash
# 이미지 관련
docker images                    # 로컬 이미지 목록
docker pull python:3.11         # 이미지 다운로드
docker rmi IMAGE_ID             # 이미지 삭제

# 컨테이너 관련
docker ps                       # 실행 중인 컨테이너 목록
docker ps -a                    # 모든 컨테이너 목록
docker run IMAGE                # 컨테이너 실행
docker stop CONTAINER_ID        # 컨테이너 중지
docker rm CONTAINER_ID          # 컨테이너 삭제
docker logs CONTAINER_ID        # 컨테이너 로그 확인

# 시스템 정리
docker system prune -a          # 사용하지 않는 리소스 삭제
```

---

## 5.2 Dockerfile 작성

### 5.3.1 기본 Dockerfile

**단일 파일 FastAPI 앱을 위한 Dockerfile**:

```dockerfile
# Dockerfile
FROM python:3.11

WORKDIR /code

# 의존성 파일 복사 (캐싱 최적화)
COPY ./requirements.txt /code/requirements.txt

# 의존성 설치
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 앱 코드 복사
COPY ./app /code/app

# 컨테이너 실행 시 실행할 명령
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
```

**requirements.txt**:

```txt
fastapi[standard]>=0.115.0
uvicorn[standard]>=0.30.0
```

### 5.3.2 Poetry 프로젝트를 위한 Dockerfile

**2단계에서 만든 Poetry 프로젝트 컨테이너화**:

```dockerfile
# Dockerfile
FROM python:3.11

# Poetry 설치
RUN pip install --no-cache-dir poetry==2.2.1

WORKDIR /code

# Poetry 설정 (가상환경 생성 안 함)
ENV POETRY_VIRTUALENVS_CREATE=false

# 의존성 파일만 먼저 복사 (캐싱 최적화)
COPY pyproject.toml poetry.lock /code/

# 의존성 설치 (개발 의존성 제외)
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# 앱 코드 복사
COPY ./kaira_fastapi_poetry /code/kaira_fastapi_poetry

# 정적 파일 복사 (있는 경우)
COPY ./kaira-1.0.0 /code/kaira-1.0.0

# 포트 노출
EXPOSE 80

# 앱 실행
CMD ["uvicorn", "kaira_fastapi_poetry.main:app", "--host", "0.0.0.0", "--port", "80"]
```

### 5.3.3 Dockerfile 명령어 설명

| 명령어      | 설명                        | 예시                                    |
| ----------- | --------------------------- | --------------------------------------- |
| `FROM`    | 베이스 이미지 지정          | `FROM python:3.11`                    |
| `WORKDIR` | 작업 디렉토리 설정          | `WORKDIR /code`                       |
| `COPY`    | 파일/디렉토리 복사          | `COPY ./app /code/app`                |
| `RUN`     | 명령어 실행 (빌드 시)       | `RUN pip install -r requirements.txt` |
| `ENV`     | 환경 변수 설정              | `ENV PYTHONUNBUFFERED=1`              |
| `EXPOSE`  | 포트 문서화                 | `EXPOSE 80`                           |
| `CMD`     | 컨테이너 실행 명령 (런타임) | `CMD ["uvicorn", "main:app"]`         |

### 5.3.4 멀티 스테이지 빌드 (최적화 - 2024 Best Practices)

**이미지 크기를 줄이는 최신 기법** (Docker 27.x 지원):

```dockerfile
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
RUN poetry install --no-root --only main

# === 2단계: Runtime (최소 이미지) ===
FROM python:3.11-slim

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

WORKDIR /app

# Builder에서 설치된 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 앱 코드 복사
COPY ./src ./src
COPY ./src/kaira_fastapi_poetry/kaira-1.0.0 ./kaira-1.0.0

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

```

**주요 개선 사항 (2024 Best Practices)**:

| 개선 사항                           | 효과                                               |
| ----------------------------------- | -------------------------------------------------- |
| `--no-interaction`, `--no-ansi` | Poetry 일관성 보장                                 |
| `--only main` (그룹 지정)         | 빌드 도구 제외, 이미지 크기 감소                   |
| `PYTHONDONTWRITEBYTECODE=1`       | `.pyc` 파일 방지                                 |
| `PYTHONUNBUFFERED=1`              | 실시간 로그 출력                                   |
| `useradd -u 1000`                 | UID 명시 (프로덕션 호환성)                         |
| `python:3.11-slim`                | `full` 대신 `slim` 사용 (이미지 크기 70% 감소) |

**이미지 크기 비교**:

```
python:3.11 (full):     1.0 GB
python:3.11-slim:       150 MB  (↓ 85%)
위 최적화 이후:          ~300 MB (↓ 70%)
```

---

## 5.3 이미지 빌드와 실행

### 5.4.1 이미지 빌드

**기본 빌드**:

```bash
# 현재 디렉토리에서 빌드 (태그: kaira-server)
docker build -t kaira-server .

# 특정 Dockerfile 지정
docker build -t kaira-server -f Dockerfile.prod .

# 빌드 완료 확인
docker images | grep kaira-server
```

**출력 예시**:

```
[+] Building 45.3s (12/12) FINISHED
=> [1/6] FROM docker.io/library/python:3.11
=> [2/6] COPY ./requirements.txt /code/requirements.txt
=> [3/6] RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
=> [4/6] COPY ./app /code/app
=> exporting to image
=> => naming to docker.io/library/kaira-server
```

### 5.4.2 컨테이너 실행

**기본 실행**:

```bash
# 기본 실행 (터미널 블로킹)
docker run -p 8000:80 kaira-server

# 백그라운드 실행 (-d: detached)
docker run -d -p 8000:80 --name kaira-container kaira-server

# 실행 확인
docker ps
```

**포트 매핑**:

- `-p HOST_PORT:CONTAINER_PORT`
- 예: `-p 8000:80` → 호스트의 8000번 포트를 컨테이너의 80번 포트로 연결

### 5.4.3 환경 변수 전달

```bash
# 단일 환경 변수
docker run -d -p 8000:80 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  kaira-server

# .env 파일 사용
docker run -d -p 8000:80 \
  --env-file .env.production \
  kaira-server
```

### 5.4.4 볼륨 마운트

**개발 중 코드 변경 즉시 반영**:

```bash
# 로컬 디렉토리를 컨테이너에 마운트
docker run -d -p 8000:80 \
  -v $(pwd)/app:/code/app \
  kaira-server

# 정적 파일 마운트
docker run -d -p 8000:80 \
  -v $(pwd)/kaira-1.0.0:/code/kaira-1.0.0 \
  kaira-server
```

### 5.4.5 컨테이너 관리

```bash
# 로그 확인
docker logs kaira-container

# 실시간 로그 (tail -f 같은 효과)
docker logs -f kaira-container

# 컨테이너 내부 접속
docker exec -it kaira-container bash

# 컨테이너 중지
docker stop kaira-container

# 컨테이너 삭제
docker rm kaira-container

# 이미지와 컨테이너 한 번에 삭제
docker rm -f kaira-container
docker rmi kaira-server
```

---

## 5.4 docker-compose 활용

### 5.5.1 docker-compose란?

여러 컨테이너를 YAML 파일로 정의하고 한 번에 관리하는 도구입니다.

**장점**:

- ✅ 복잡한 docker run 명령을 간단하게
- ✅ 여러 서비스를 한 번에 시작/중지
- ✅ 네트워크와 볼륨 자동 생성
- ✅ 환경별 설정 분리 가능

### 5.5.2 기본 docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    container_name: kaira-server
    ports:
      - "8000:80"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
    volumes:
      - ./app:/code/app
      - ./kaira-1.0.0:/code/kaira-1.0.0
    restart: unless-stopped
```

**실행**:

```bash
# 백그라운드 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 중지
docker-compose down

# 중지 + 볼륨 삭제
docker-compose down -v
```

### 5.5.3 개발/운영 환경 분리

**docker-compose.yml (공통 설정)**:

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    container_name: kaira-server
    ports:
      - "${PORT:-8000}:80"
    environment:
      - ENVIRONMENT=${ENVIRONMENT:-development}
```

**docker-compose.dev.yml (개발 환경)**:

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    volumes:
      - ./app:/code/app
      - ./kaira-1.0.0:/code/kaira-1.0.0
    environment:
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    command: ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
```

**docker-compose.prod.yml (운영 환경)**:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    environment:
      - DEBUG=false
      - LOG_LEVEL=WARNING
    restart: always
    # 프로덕션에서는 볼륨 마운트 제거
```

**실행 방법**:

```bash
# 개발 환경
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# 운영 환경
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 5.5.4 멀티 서비스 구성

**FastAPI + PostgreSQL + Redis 예제**:

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    container_name: kaira-server
    ports:
      - "8000:80"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/kaira
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    container_name: kaira-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=kaira
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    container_name: kaira-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**실행**:

```bash
# 모든 서비스 시작
docker-compose up -d

# 특정 서비스만 시작
docker-compose up -d app

# 모든 서비스 상태 확인
docker-compose ps

# 특정 서비스 로그 확인
docker-compose logs -f app
```

### 5.5.5 헬스 체크 추가

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:80"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**앱에 헬스 체크 엔드포인트 추가** (`app/main.py`):

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
```

---

## 5.5 최적화와 Best Practices

### 5.6.1 빌드 캐시 최적화

**나쁜 예** (매번 모든 의존성 재설치):

```dockerfile
# ❌ 비효율적
COPY . /code
RUN pip install -r requirements.txt
```

**좋은 예** (의존성 파일만 먼저 복사):

```dockerfile
# ✅ 효율적
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code
```

### 5.6.2 이미지 크기 최소화

**1. Slim 베이스 이미지 사용**:

```dockerfile
# ❌ 1.2GB
FROM python:3.11

# ✅ 300MB
FROM python:3.11-slim

# ✅ 50MB (alpine은 호환성 문제 주의)
FROM python:3.11-alpine
```

**2. 불필요한 파일 제외 (.dockerignore)**:

```text
# .dockerignore
**/__pycache__
**/*.pyc
**/.pytest_cache
**/.venv
**/venv
**/.git
**/node_modules
**/.env
**/logs
```

**3. 멀티 스테이지 빌드**:

```dockerfile
# ✅ 빌드 도구와 런타임 분리
FROM python:3.11 as builder
RUN pip install ...

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
```

### 5.6.3 보안 Best Practices

**1. 비root 사용자로 실행**:

```dockerfile
# 사용자 생성
RUN useradd -m -u 1000 appuser

# 파일 소유권 변경
RUN chown -R appuser:appuser /code

# 사용자 전환
USER appuser
```

**2. 민감 정보 제외**:

```dockerfile
# ❌ 절대 하지 말 것
ENV API_KEY=sk-abc123...

# ✅ 런타임에 주입
# docker run -e API_KEY=$API_KEY ...
```

**3. 버전 고정**:

```dockerfile
# ❌ 불안정
FROM python:3.11

# ✅ 안정적
FROM python:3.11.8-slim

# requirements.txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

### 5.6.4 로깅 Best Practices

```dockerfile
# stdout/stderr로 로그 출력 (Docker 로그 수집 가능)
ENV PYTHONUNBUFFERED=1

# 로그 레벨 환경 변수로 제어
ENV LOG_LEVEL=INFO
```

**앱 코드**:

```python
import logging
import os

# 환경 변수로 로그 레벨 제어
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=log_level)
```

### 5.6.5 성능 최적화

**Uvicorn Workers 설정**:

```dockerfile
# CPU 코어 수에 맞춰 worker 개수 설정
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
```

**docker-compose에서 리소스 제한**:

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
        reservations:
          cpus: '1'
          memory: 512M
```

---

## 5.6 로컬 개발 환경 구성

### 5.7.1 개발용 Dockerfile

```dockerfile
# Dockerfile.dev
FROM python:3.11

WORKDIR /code

# Poetry 설치
RUN pip install poetry==1.8.5

ENV POETRY_VIRTUALENVS_CREATE=false

# 의존성 설치 (개발 의존성 포함)
COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-root

# 코드는 볼륨 마운트로 제공 (별도 COPY 불필요)

# 개발 서버 실행 (--reload 옵션)
CMD ["uvicorn", "kaira_fastapi_poetry.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
```

### 5.7.2 개발용 docker-compose

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - ./kaira_fastapi_poetry:/code/kaira_fastapi_poetry
      - ./kaira-1.0.0:/code/kaira-1.0.0
      - ./tests:/code/tests
    ports:
      - "8000:80"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    stdin_open: true
    tty: true
```

**실행**:

```bash
# 개발 환경 시작
docker-compose -f docker-compose.dev.yml up

# 코드 변경 시 자동 재시작 (--reload 덕분)
```

### 5.7.3 VS Code Dev Container 설정

**.devcontainer/devcontainer.json**:

```json
{
  "name": "Kaira FastAPI Dev",
  "dockerComposeFile": "../docker-compose.dev.yml",
  "service": "app",
  "workspaceFolder": "/code",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff"
      ]
    }
  }
}
```

---

## 5.7 프로덕션 배포 준비

### 5.8.1 프로덕션 Dockerfile

```dockerfile
# Dockerfile.prod
FROM python:3.11-slim as builder

RUN pip install --no-cache-dir poetry==1.8.5

WORKDIR /code

ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock /code/
RUN poetry install --no-root --no-dev --no-interaction --no-ansi

# === Runtime Stage ===
FROM python:3.11-slim

WORKDIR /code

# builder에서 설치된 패키지 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# 앱 코드 복사
COPY ./kaira_fastapi_poetry /code/kaira_fastapi_poetry
COPY ./kaira-1.0.0 /code/kaira-1.0.0

# 비root 사용자 생성
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /code

USER appuser

EXPOSE 80

# 프로덕션 설정
ENV ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1

# 여러 worker로 실행
CMD ["uvicorn", "kaira_fastapi_poetry.main:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4"]
```

### 5.8.2 프로덕션 docker-compose

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    container_name: kaira-server
    ports:
      - "80:80"
    environment:
      - ENVIRONMENT=production
      - DEBUG=false
      - LOG_LEVEL=WARNING
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:80/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G

  nginx:
    image: nginx:alpine
    container_name: kaira-nginx
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - app
    restart: always
```

### 5.8.3 Nginx 리버스 프록시 설정

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream fastapi_backend {
        server app:80;
    }

    server {
        listen 80;
        server_name kaira.example.com;

        location / {
            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        location /static/ {
            alias /usr/share/nginx/html/static/;
        }
    }
}
```

### 5.8.4 CI/CD 파이프라인 예제

**.github/workflows/docker-deploy.yml**:

```yaml
name: Build and Deploy Docker

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
    
      - name: Build Docker Image
        run: docker build -t kaira-server:${{ github.sha }} -f Dockerfile.prod .
    
      - name: Run Tests
        run: |
          docker run --rm kaira-server:${{ github.sha }} pytest
    
      - name: Push to Registry
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
          docker tag kaira-server:${{ github.sha }} yourusername/kaira-server:latest
          docker push yourusername/kaira-server:latest
```

---

## 5.8 문제 해결

### 5.9.1 자주 발생하는 문제

#### 문제 1: "Cannot connect to Docker daemon"

**증상**:

```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**해결**:

```bash
# Docker 데몬 시작
sudo systemctl start docker

# Docker Desktop 실행 (macOS/Windows)
# Docker Desktop 앱 실행 확인
```

#### 문제 2: 포트 충돌

**증상**:

```
Error: Port 8000 is already in use
```

**해결**:

```bash
# 다른 포트 사용
docker run -p 8001:80 kaira-server

# 또는 기존 프로세스 종료
lsof -ti:8000 | xargs kill -9
```

#### 문제 3: 빌드 캐시 문제

**증상**:

```
의존성을 업데이트했는데 반영이 안 됨
```

**해결**:

```bash
# 캐시 없이 빌드
docker build --no-cache -t kaira-server .

# 또는 docker-compose
docker-compose build --no-cache
```

#### 문제 4: 볼륨 권한 문제

**증상**:

```
Permission denied: '/code/app'
```

**해결**:

```dockerfile
# Dockerfile에서 권한 설정
RUN chown -R appuser:appuser /code
USER appuser
```

### 5.9.2 디버깅 팁

```bash
# 컨테이너 내부 확인
docker exec -it kaira-container bash

# 실시간 로그 확인
docker logs -f kaira-container

# 컨테이너 리소스 사용량 확인
docker stats kaira-container

# 이미지 레이어 확인
docker history kaira-server

# 네트워크 확인
docker network ls
docker network inspect bridge
```

### 5.9.3 성능 문제

**빌드가 느릴 때**:

```bash
# 빌드킷 사용 (더 빠른 빌드)
DOCKER_BUILDKIT=1 docker build -t kaira-server .

# 멀티 스테이지 빌드 활용
```

**컨테이너가 느릴 때**:

```yaml
# docker-compose.yml에서 리소스 제한 완화
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 2G
```

---

## 5.9 체크리스트

프로젝트에 다음 항목들이 구현되었는지 확인하세요:

### Docker 기초

- [ ] Docker Desktop/Engine 설치 완료
- [ ] `docker --version` 확인
- [ ] 기본 Docker 명령어 이해 (run, build, ps, logs)

### Dockerfile

- [ ] 기본 Dockerfile 작성
- [ ] `.dockerignore` 파일 작성
- [ ] 빌드 캐시 최적화 (의존성 파일 먼저 복사)
- [ ] 멀티 스테이지 빌드 적용 (선택사항)
- [ ] 비root 사용자로 실행
- [ ] 버전 고정 (Python, 패키지)

### 이미지 빌드

- [ ] 이미지 빌드 성공
- [ ] 이미지 크기 최적화
- [ ] 태그 전략 수립 (latest, version)

### 컨테이너 실행

- [ ] 로컬에서 컨테이너 실행 성공
- [ ] 포트 매핑 확인
- [ ] 환경 변수 전달 테스트
- [ ] 헬스 체크 엔드포인트 추가

### docker-compose

- [ ] `docker-compose.yml` 작성
- [ ] 개발/운영 환경 분리
- [ ] 멀티 서비스 구성 (필요 시)
- [ ] 볼륨 설정
- [ ] 네트워크 설정

### 최적화

- [ ] Slim 베이스 이미지 사용
- [ ] 불필요한 파일 제외 (.dockerignore)
- [ ] 로깅 설정 (PYTHONUNBUFFERED=1)
- [ ] 리소스 제한 설정

### 프로덕션

- [ ] 프로덕션 Dockerfile 작성
- [ ] Nginx 리버스 프록시 설정 (선택사항)
- [ ] CI/CD 파이프라인 구성 (선택사항)
- [ ] 보안 점검 (비root 사용자, 버전 고정)

### 문서화

- [ ] README에 Docker 빌드/실행 방법 추가
- [ ] 환경 변수 목록 문서화
- [ ] 트러블슈팅 가이드 작성

---

## 📚 다음 단계

4단계를 완료했다면, 이제 다음을 진행할 수 있습니다:

1. **5단계: 클라우드 배포** (`05_CLOUD_DEPLOYMENT_GUIDE.md`)

   - AWS EC2에 Docker 컨테이너 배포
   - GCP App Engine 대안
   - 도메인 연결과 SSL 인증서
   - 모니터링과 로깅
2. **로컬 테스트**:

   ```bash
   # Docker 이미지 빌드
   docker build -t kaira-server .

   # 컨테이너 실행
   docker run -d -p 8000:80 kaira-server

   # 접속 테스트
   curl http://localhost:8000
   ```
3. **docker-compose로 전체 스택 실행**:

   ```bash
   docker-compose up -d
   docker-compose logs -f
   ```

---

## 🎯 핵심 요약

이번 단계에서 배운 내용:

1. **Docker 기초**: 이미지, 컨테이너, Dockerfile, Registry
2. **Dockerfile 작성**: 효율적인 레이어 구성, 캐싱 최적화
3. **멀티 스테이지 빌드**: 이미지 크기 최소화
4. **docker-compose**: 멀티 서비스 오케스트레이션
5. **Best Practices**: 보안, 성능, 로깅

**핵심 명령어**:

```bash
# 빌드
docker build -t kaira-server .

# 실행
docker run -d -p 8000:80 kaira-server

# docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

이제 어디서든 동일하게 실행되는 컨테이너화된 FastAPI 애플리케이션을 만들 수 있습니다! 🎉

---

**작성일**: 2025-01-XX
**최종 검증**: Docker 27.x, docker-compose 2.x, FastAPI 0.115.x
