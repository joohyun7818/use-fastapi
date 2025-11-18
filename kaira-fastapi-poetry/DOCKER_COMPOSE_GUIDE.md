# Docker Compose 실행 가이드

## 📋 사전 요구사항

1. Docker 이미지가 로컬에 빌드되어 있어야 함
2. Docker와 Docker Compose가 설치되어 있어야 함

## 🔨 Step 1: 로컬 이미지 빌드 (첫 실행 시만)

```bash
docker build -t kaira-fastapi:latest -f Dockerfile .
```

## 🚀 Step 2: Docker Compose로 실행

### 기본 실행
```bash
docker-compose up
```

### 백그라운드 실행
```bash
docker-compose up -d
```

### 로그 확인
```bash
docker-compose logs -f
```

### 특정 서비스의 로그 확인
```bash
docker-compose logs -f kaira-api      # FastAPI 서버 로그
docker-compose logs -f postgres       # PostgreSQL 로그
docker-compose logs -f pgadmin        # pgAdmin 로그
```

## 🛑 Step 3: Docker Compose 중지

```bash
# 컨테이너 중지
docker-compose down

# 데이터 삭제하면서 중지
docker-compose down -v
```

## 📊 구성 정보

### 서비스
| 서비스 | 포트 | 설명 |
|--------|------|------|
| kaira-api | 8000 | FastAPI 서버 |
| postgres | 5432 | PostgreSQL 데이터베이스 |
| pgadmin | 5050 | PostgreSQL GUI 관리 도구 |

### 접속 URL
- **FastAPI**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

### 데이터베이스 연결 정보
- **Host**: postgres (컨테이너 내부), localhost (호스트 OS)
- **Port**: 5432
- **User**: Kaira_user
- **Password**: kaira_1234
- **Database**: kaira_db

## 🔧 환경 변수 커스터마이징

`.env` 파일에서 다음 변수를 수정할 수 있습니다:

```properties
# FastAPI 포트
API_PORT=8000

# PostgreSQL 설정
POSTGRES_USER=Kaira_user
POSTGRES_PASSWORD=kaira_1234
POSTGRES_DB=kaira_db
POSTGRES_PORT=5432

# pgAdmin 설정
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin
PGADMIN_PORT=5050
```

변수 수정 후 다시 실행하면 적용됩니다:
```bash
docker-compose down
docker-compose up -d
```

## 🐛 문제 해결

### 1️⃣ "Cannot find image 'kaira-fastapi:latest'" 오류
→ 로컬 이미지를 빌드해야 함
```bash
docker build -t kaira-fastapi:latest -f Dockerfile .
```

### 2️⃣ 포트가 이미 사용 중인 경우
→ `.env` 파일에서 포트 번호 변경
```properties
API_PORT=8001        # 8000 → 8001로 변경
POSTGRES_PORT=5433   # 5432 → 5433으로 변경
PGADMIN_PORT=5051    # 5050 → 5051로 변경
```

### 3️⃣ 데이터베이스 초기화
→ 볼륨을 삭제하고 다시 시작
```bash
docker-compose down -v
docker-compose up -d
```

### 4️⃣ 이미지가 최신 상태가 아닌 경우
→ 이미지를 다시 빌드
```bash
docker build -t kaira-fastapi:latest --no-cache -f Dockerfile .
docker-compose up -d --force-recreate
```

## 📌 팁

### 컨테이너에 직접 접속
```bash
# FastAPI 서버에 접속
docker exec -it kaira-api bash

# PostgreSQL에 접속
docker exec -it kaira_postgres psql -U Kaira_user -d kaira_db

# pgAdmin에 접속
docker exec -it kaira_pgadmin bash
```

### 데이터베이스 상태 확인
```bash
docker-compose ps
```

### 네트워크 확인
```bash
docker network ls
docker network inspect kaira_network
```

## 🎯 일반적인 워크플로우

```bash
# 1. 로컬 이미지 빌드
docker build -t kaira-fastapi:latest -f Dockerfile .

# 2. Docker Compose로 실행
docker-compose up -d

# 3. 로그 확인
docker-compose logs -f

# 4. API 테스트
curl http://localhost:8000/

# 5. pgAdmin에서 DB 관리
# http://localhost:5050에 접속하여 admin@example.com / admin으로 로그인

# 6. 종료
docker-compose down
```
