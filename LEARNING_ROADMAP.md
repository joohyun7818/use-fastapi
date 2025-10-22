# FastAPI 학습 로드맵: CLI → Poetry → 데이터베이스 → 클라우드 배포

**목표**: 정적 웹사이트(`kaira-1.0.0`)를 FastAPI로 서빙하고, 데이터베이스를 연동하여 클라우드 인스턴스에 배포하기

**총 학습 기간**: 3-5주 (개인 공부 페이스 기준, 데이터베이스 포함)

---

## 📊 전체 학습 맵

```
┌─────────────────────────────────────────────────────────────┐
│ 1단계: FastAPI-CLI (기초 프로토타입)                         │
│ └─ 2-3일 / 포커스: FastAPI 핵심 개념                        │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 2단계: Poetry (프로덕션 구조)                               │
│ └─ 2-3일 / 포커스: 의존성 관리 + 프로젝트 구조             │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 3단계: 로컬 테스트 및 최적화                                 │
│ └─ 3-5일 / 포커스: 테스트, 에러 처리, 로깅                │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 4단계: 데이터베이스 연결 및 관리                            │
│ └─ 5-7일 / 포커스: SQLAlchemy, PostgreSQL, 마이그레이션    │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 5단계: Docker 컨테이너화                                    │
│ └─ 2-3일 / 포커스: Dockerfile, docker-compose               │
└─────────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ 6단계: 클라우드 배포 (AWS/GCP)                             │
│ └─ 3-5일 / 포커스: EC2/App Engine, 도메인, SSL              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 1단계: FastAPI-CLI로 빠른 프로토타입 만들기

**시간**: 2-3일  
**난이도**: ⭐ (쉬움)  
**학습 내용**: FastAPI 기초, 라우팅, 정적 파일 서빙, Uvicorn

### 1.1 FastAPI-CLI 설치 및 프로젝트 생성
```bash
# 이미 설치되어 있는지 확인
fastapi --version

# 새 프로젝트 생성
fastapi new kaira-server

# 자동 생성된 구조 확인
cd kaira-server
ls -la
```

**생성 구조**:
```
kaira-server/
├── main.py              # FastAPI 앱 진입점
├── requirements.txt     # 의존성
└── tests/
    └── test_main.py
```

### 1.2 기본 엔드포인트 작성
```python
# main.py 예시
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Kaira Server")

@app.get("/")
def read_root():
    return {"message": "Welcome to Kaira!"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# 정적 파일 마운트
app.mount("/static", StaticFiles(directory="../kaira-1.0.0"), name="static")
```

### 1.3 로컬에서 실행
```bash
# 자동 리로드 모드 실행
fastapi dev main.py

# 또는 표준 uvicorn
uvicorn main:app --reload --port 8000
```

### 1.4 API 문서 확인
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 1.5 학습 체크리스트
- [ ] 프로젝트 생성 및 실행 성공
- [ ] 간단한 GET 엔드포인트 작성
- [ ] 정적 파일(`kaira-1.0.0`) 마운트 성공
- [ ] Swagger UI에서 API 테스트
- [ ] `requirements.txt` 의존성 확인

---

## 🎯 2단계: Poetry로 프로덕션 구조 재구성

**시간**: 2-3일  
**난이도**: ⭐⭐ (중간)  
**학습 내용**: Poetry 워크플로우, 의존성 관리, 프로젝트 구조

### 2.1 Poetry 설치
```bash
# macOS
brew install poetry

# 설치 확인
poetry --version
```

### 2.2 Poetry 프로젝트 생성
```bash
# 새 프로젝트
poetry new kaira-fastapi-prod

cd kaira-fastapi-prod
```

**생성 구조**:
```
kaira-fastapi-prod/
├── pyproject.toml
├── poetry.lock
├── README.md
├── kaira_fastapi_prod/
│   └── __init__.py
└── tests/
    └── __init__.py
```

### 2.3 의존성 추가 (CLI 프로젝트에서 배운 내용 적용)
```bash
poetry add fastapi uvicorn[standard]
poetry add --group dev pytest pytest-cov black flake8
```

결과 - `pyproject.toml`:
```toml
[tool.poetry.dependencies]
python = "^3.10"
fastapi = "^0.120.0"
uvicorn = {version = "^0.30.0", extras = ["standard"]}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^24.0.0"
flake8 = "^7.0.0"
```

### 2.4 프로덕션 폴더 구조로 확장
```
kaira-fastapi-prod/
├── kaira_fastapi_prod/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱 진입점
│   ├── config.py            # 설정
│   ├── middleware.py        # 커스텀 미들웨어
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── endpoints.py     # 엔드포인트 모음
│   │
│   ├── static/              # 정적 파일 (또는 심볼릭 링크)
│   │   └── kaira-1.0.0/
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_endpoints.py
│
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

### 2.5 Poetry 가상환경으로 실행
```bash
poetry shell

uvicorn kaira_fastapi_prod.main:app --reload --port 8000
```

### 2.6 학습 체크리스트
- [ ] Poetry 설치 및 프로젝트 생성
- [ ] 의존성 추가 및 `pyproject.toml` 이해
- [ ] Poetry 가상환경 진입 및 실행
- [ ] CLI 프로젝트 코드 → Poetry 프로젝트로 마이그레이션
- [ ] Swagger UI 동작 확인

---

## 🎯 3단계: 로컬 테스트 및 최적화

**시간**: 3-5일  
**난이도**: ⭐⭐ (중간)  
**학습 내용**: 유닛 테스트, 에러 핸들링, 로깅, 환경 변수

### 3.1 테스트 작성
```python
# tests/test_main.py
from fastapi.testclient import TestClient
from kaira_fastapi_prod.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
```

테스트 실행:
```bash
poetry run pytest tests/ -v

# 커버리지 확인
poetry run pytest tests/ --cov=kaira_fastapi_prod
```

### 3.2 에러 핸들링 추가
```python
# kaira_fastapi_prod/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Invalid ID")
    return {"item_id": item_id}
```

### 3.3 로깅 설정
```python
# kaira_fastapi_prod/config.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
```

### 3.4 환경 변수 관리
```bash
# .env 파일
DEBUG=True
PORT=8000
STATIC_PATH=./kaira-1.0.0
```

```python
# kaira_fastapi_prod/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    debug: bool = False
    port: int = 8000
    static_path: str = "./kaira-1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 3.5 학습 체크리스트
- [ ] 유닛 테스트 작성 및 실행
- [ ] 테스트 커버리지 70% 이상 달성
- [ ] 에러 핸들링 구현
- [ ] 로깅 시스템 통합
- [ ] 환경 변수 관리 설정

---

## 🎯 4단계: Docker 컨테이너화

**시간**: 2-3일  
**난이도**: ⭐⭐⭐ (중상)  
**학습 내용**: Dockerfile, 이미지 빌드, 컨테이너 실행

### 4.1 Dockerfile 작성
```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Poetry 설치
RUN pip install poetry

# 의존성 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치
RUN poetry install --no-dev

# 앱 코드 복사
COPY . .

# 포트 노출
EXPOSE 8000

# 실행
CMD ["poetry", "run", "uvicorn", "kaira_fastapi_prod.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4.2 .dockerignore 작성
```
.git
__pycache__
*.pyc
*.pyo
.env
.venv
venv/
dist/
build/
*.egg-info/
.pytest_cache/
.coverage
```

### 4.3 이미지 빌드 및 실행
```bash
# 이미지 빌드
docker build -t kaira-fastapi:latest .

# 컨테이너 실행
docker run -p 8000:8000 kaira-fastapi:latest

# 또는 백그라운드 실행
docker run -d -p 8000:8000 --name kaira kaira-fastapi:latest
```

### 4.4 docker-compose (다중 서비스 관리)
```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
    volumes:
      - ./kaira-1.0.0:/app/kaira-1.0.0:ro
```

실행:
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### 4.5 학습 체크리스트
- [ ] Dockerfile 작성 및 이미지 빌드 성공
- [ ] 로컬 Docker 컨테이너에서 앱 실행 확인
- [ ] docker-compose로 다중 서비스 관리
- [ ] 환경 변수 Docker에 전달
- [ ] 스태틱 파일 마운트 확인

---

## 🎯 5단계: 클라우드 배포 (AWS/GCP)

**시간**: 3-5일  
**난이도**: ⭐⭐⭐⭐ (상)  
**학습 내용**: 클라우드 플랫폼, CI/CD, 모니터링

### 5.1 AWS EC2 배포 (추천: 저비용)

#### 5.1.1 EC2 인스턴스 생성
- AWS 콘솔 → EC2 → 인스턴스 시작
- AMI: Ubuntu 22.04 LTS
- 인스턴스 타입: t2.micro (프리 티어)
- 보안 그룹: SSH(22), HTTP(80), HTTPS(443), 8000(앱)

#### 5.1.2 SSH로 접속
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### 5.1.3 서버 세팅
```bash
# 업데이트
sudo apt update && sudo apt upgrade -y

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 사용자에게 Docker 권한 부여
sudo usermod -aG docker ubuntu

# 로그아웃 후 재접속
exit
```

#### 5.1.4 앱 배포
```bash
# 앱 클론 (또는 ZIP 업로드)
git clone https://your-repo.git
cd kaira-fastapi-prod

# Docker 컴포즈로 실행
docker-compose up -d

# 로그 확인
docker-compose logs -f
```

### 5.2 Nginx 리버스 프록시 (선택, 프로덕션 권장)
```bash
# Nginx 설치
sudo apt install nginx -y

# 설정 파일
sudo nano /etc/nginx/sites-available/default
```

```nginx
# /etc/nginx/sites-available/default
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Nginx 재시작
sudo systemctl restart nginx
```

### 5.3 도메인 및 SSL 연결 (Let's Encrypt)
```bash
# Certbot 설치
sudo apt install certbot python3-certbot-nginx -y

# SSL 인증서 발급
sudo certbot --nginx -d your-domain.com

# 자동 갱신 설정
sudo systemctl enable certbot.timer
```

### 5.4 모니터링 및 로깅
```bash
# 앱 로그 확인
docker-compose logs -f app

# 시스템 리소스 모니터링
top
df -h
```

### 5.5 GCP App Engine 배포 (선택, 서버리스)
```bash
# app.yaml 작성
cat > app.yaml <<EOF
runtime: python310
entrypoint: gunicorn -w 4 -b 0.0.0.0:8080 kaira_fastapi_prod.main:app
EOF

# 배포
gcloud app deploy
```

### 5.6 CI/CD 파이프라인 (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build and push Docker image
        run: |
          docker build -t kaira-fastapi:${{ github.sha }} .
          # ECR에 푸시
          
      - name: Deploy to EC2
        run: |
          # SSH로 배포 명령 실행
```

### 5.7 학습 체크리스트
- [ ] 클라우드 계정 생성 (AWS 또는 GCP)
- [ ] 인스턴스 생성 및 SSH 접속
- [ ] Docker 및 필요 도구 설치
- [ ] 앱 배포 및 정상 작동 확인
- [ ] 도메인 연결 (Route53 또는 DNS)
- [ ] SSL 인증서 설치
- [ ] 모니터링 대시보드 구성
- [ ] CI/CD 파이프라인 설정 (선택)

---

## 📝 추가 학습 리소스

| 주제 | 리소스 |
|------|--------|
| FastAPI 공식 문서 | https://fastapi.tiangolo.com |
| Poetry 문서 | https://python-poetry.org |
| Docker 가이드 | https://docs.docker.com |
| AWS EC2 | https://docs.aws.amazon.com/ec2 |
| GCP App Engine | https://cloud.google.com/appengine |

---

## ✅ 전체 체크리스트

### 1단계 완료 기준
- FastAPI-CLI로 프로토타입 실행
- Swagger UI 정상 작동

### 2단계 완료 기준
- Poetry 프로젝트 구조 완성
- 모든 엔드포인트 작동

### 3단계 완료 기준
- 테스트 커버리지 70% 이상
- 에러 핸들링 + 로깅 통합

### 4단계 완료 기준
- Docker 이미지 빌드 성공
- docker-compose로 로컬 실행 성공

### 5단계 완료 기준
- 클라우드 인스턴스 배포 완료
- 공개 URL에서 앱 접근 가능
- SSL 인증서 설치
- 모니터링 및 로깅 작동

---

## 💡 학습 팁

1. **각 단계별로 Git 커밋**: 진행 상황 추적 용이
2. **매일 15-30분 복습**: 이전 단계 복습
3. **에러 메시지 읽기**: Google 검색 전에 에러를 자세히 읽기
4. **공식 문서 활용**: ChatGPT보다 공식 문서 우선
5. **손으로 코드 쓰기**: 복사-붙여넣기 피하기
6. **로그 남기기**: 각 단계별 배운 점 정리

---

## 🚀 예상 완료 시간
- **최소**: 2주 (빠른 페이스)
- **권장**: 3-4주 (깊이 있는 학습)
- **충분**: 4-6주 (추가 실습 포함)

여기까지 모두 완료하면, **프로덕션급 FastAPI 애플리케이션을 클라우드에서 운영할 수 있는 능력**을 갖추게 됩니다! 🎉
