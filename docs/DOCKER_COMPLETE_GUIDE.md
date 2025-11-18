# 🐳 Docker 완벽 가이드

> FastAPI 개발부터 프로덕션 배포까지, Docker의 모든 것을 정리한 완벽 가이드

**목차**
1. [도커 핵심 개념 & 기술 + 사용 이유](#1-도커-핵심-개념--기술--사용-이유)
2. [도커 이미지 생성 방법](#2-도커-이미지-생성-방법)
3. [도커 컴포즈 사용 방법](#3-도커-컴포즈-사용-방법)
4. [도커 Build를 사용한 이미지 경량화](#4-도커-build를-사용한-이미지-경량화)

---

# 1. 도커 핵심 개념 & 기술 + 사용 이유

## 1.1 Docker란?

**Docker**는 애플리케이션을 **컨테이너**라는 표준화된 단위로 패키징하고 실행하는 플랫폼입니다.

### 🎯 핵심 개념 5가지

#### 1️⃣ **이미지 (Image)**

- 애플리케이션 실행에 필요한 모든 것의 **템플릿**
- OS, 라이브러리, 코드, 설정 등을 포함
- 변경 불가능한 **읽기 전용** 파일시스템

```bash
# 이미지 관련 명령어
docker images                    # 로컬 이미지 목록
docker pull python:3.11         # 이미지 다운로드
docker rmi IMAGE_ID             # 이미지 삭제
docker history IMAGE_NAME       # 이미지 레이어 확인
```

#### 2️⃣ **컨테이너 (Container)**

- 이미지를 **실행한 인스턴스**
- 격리된 환경에서 독립적으로 실행
- 변경 가능한 **읽기/쓰기** 레이어 추가

```bash
# 컨테이너 관련 명령어
docker ps                       # 실행 중인 컨테이너
docker ps -a                    # 모든 컨테이너
docker run IMAGE                # 컨테이너 실행
docker stop CONTAINER_ID        # 컨테이너 중지
docker rm CONTAINER_ID          # 컨테이너 삭제
docker logs CONTAINER_ID        # 로그 확인
docker exec -it CONTAINER bash  # 컨테이너 접속
```

#### 3️⃣ **Dockerfile**

- 이미지를 만드는 **레시피**
- 단계별 명령어로 이미지 구성
- 재현 가능하고 버전 관리 가능

```dockerfile
FROM python:3.11-slim           # 기본 이미지
WORKDIR /app                    # 작업 디렉토리
COPY requirements.txt .         # 파일 복사
RUN pip install -r requirements.txt  # 명령 실행
COPY ./app .                    # 앱 코드 복사
CMD ["python", "main.py"]       # 실행 명령
```

#### 4️⃣ **Registry (레지스트리)**

- 이미지를 저장하고 공유하는 **저장소**
- Docker Hub (공개), ECR (AWS), GCR (Google) 등
- GitHub처럼 이미지를 push/pull

```bash
# Registry 관련 명령어
docker login                    # 레지스트리 로그인
docker push USERNAME/IMAGE:TAG  # 이미지 푸시
docker pull USERNAME/IMAGE:TAG  # 이미지 풀
```

#### 5️⃣ **Layer (레이어)**

- 이미지는 여러 **레이어의 스택**
- 각 레이어는 이전 상태의 **diff**만 저장
- 캐싱으로 빠른 빌드 및 배포

```
Dockerfile 명령어 ← → Docker 레이어
FROM python:3.11    ← → Base Image Layer
RUN pip install ... ← → Install Layer  
COPY ./app .        ← → App Code Layer
CMD ["python"]      ← → Config Layer
```

---

## 1.2 Docker Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Docker Desktop / Engine             │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │  Docker Daemon   │      │  Docker CLI      │    │
│  │  (백그라운드)    │◄────►│  (명령어 도구)   │    │
│  └──────────────────┘      └──────────────────┘    │
│           │                                          │
│           ├─ 컨테이너 실행                         │
│           ├─ 이미지 관리                           │
│           └─ 네트워크/볼륨 관리                    │
│                                                      │
└─────────────────────────────────────────────────────┘
          ▼
┌─────────────────────────────────────────────────────┐
│             컨테이너 (격리된 프로세스)              │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────────────────────────────────────┐   │
│  │  App (Python, Node.js, Java, etc)          │   │
│  ├────────────────────────────────────────────┤   │
│  │  Libraries & Dependencies                   │   │
│  ├────────────────────────────────────────────┤   │
│  │  OS Filesystem (Alpine, Ubuntu, etc)        │   │
│  └────────────────────────────────────────────┘   │
│                                                      │
│  Host와 격리된 독립적인 환경                      │
│  - 자체 프로세스 ID                               │
│  - 자체 네트워크 인터페이스                       │
│  - 자체 파일시스템                                │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 1.3 Docker vs 가상머신 (VM)

### 비교표

| 항목 | Docker | Virtual Machine |
|------|--------|-----------------|
| **크기** | 수 MB ~ 수백 MB | 수 GB |
| **시작 시간** | 밀리초 | 수 분 |
| **리소스 사용** | 가벼움 (직접 커널 사용) | 무거움 (독립 OS 실행) |
| **격리 수준** | 프로세스 레벨 | 완전 격리 |
| **포팅 가능성** | 매우 높음 | 낮음 |

### 아키텍처 비교

```
Docker 구조:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Container 1 │  │  Container 2 │  │  Container 3 │
├──────────────┤  ├──────────────┤  ├──────────────┤
│  App + Libs  │  │  App + Libs  │  │  App + Libs  │
├──────────────────────────────────────────────────┤
│          Host OS Kernel (공유)                    │
├──────────────────────────────────────────────────┤
│          Host OS (Linux/Windows/Mac)              │
└──────────────────────────────────────────────────┘

VM 구조:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Guest OS 1  │  │  Guest OS 2  │  │  Guest OS 3  │
│  + App       │  │  + App       │  │  + App       │
├──────────────┤  ├──────────────┤  ├──────────────┤
│  Hypervisor (완전 격리)                          │
├──────────────────────────────────────────────────┤
│          Host OS                                  │
└──────────────────────────────────────────────────┘
```

---

## 1.4 Docker를 사용해야 하는 이유

### 📌 문제: "나 컴퓨터에선 잘 돼요"

**시나리오**:
```
개발자: "내 Mac에서는 완벽한데?"
운영자: "서버의 Linux에서 안 됩니다..."

원인:
- 다른 Python 버전
- 다른 라이브러리 버전
- 다른 OS 설정
- 다른 환경변수
```

### ✅ 해결책: Docker

```
개발 환경 = 운영 환경 = 클라우드 환경
```

### 🎯 Docker의 이점

#### 1️⃣ **일관성 (Consistency)**

```dockerfile
# Dockerfile 한 번 작성
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./app .
CMD ["uvicorn", "main:app"]

# 결과: 모든 환경에서 동일하게 실행
```

- 개발자 로컬 환경
- CI/CD 파이프라인
- 클라우드 서버 (AWS, GCP, Azure)
- 팀원의 컴퓨터

#### 2️⃣ **격리성 (Isolation)**

```bash
# 각 컨테이너가 독립적으로 실행
docker run -d -p 5000:5000 app:v1
docker run -d -p 5001:5000 app:v2
# 같은 이미지의 다른 버전을 동시에 실행

# 한 앱의 문제가 다른 앱에 영향 없음
# 충돌 없음, 간섭 없음
```

#### 3️⃣ **이식성 (Portability)**

```bash
# 로컬에서 테스트
docker build -t myapp:latest .
docker run -d myapp:latest

# Docker Hub에 푸시
docker push myusername/myapp:latest

# 클라우드에서 풀해서 실행
docker pull myusername/myapp:latest
docker run -d myusername/myapp:latest

# 완전히 동일한 환경 자동 구성 ✅
```

#### 4️⃣ **효율성 (Efficiency)**

```
이미지 크기: 100 MB (VM은 2-5 GB)
시작 시간: 100ms (VM은 수십 초)
리소스 사용: 적음 (VM과 달리 독립 OS 안 실행)

→ 더 많은 컨테이너를 더 빠르게 실행 가능
```

#### 5️⃣ **빠른 개발 사이클**

```bash
# 코드 수정 후 재배포
docker build -t myapp:latest .
docker push myusername/myapp:latest

# 프로덕션 서버에서
docker pull myusername/myapp:latest
docker restart container

# 다운타임 최소화
```

### 📊 비용 절감

| 항목 | Without Docker | With Docker |
|------|---|---|
| **개발 시간** | 높음 (환경 설정) | 낮음 |
| **버그** | 많음 ("나 컴퓨터에선 됨") | 적음 |
| **배포 시간** | 길음 | 짧음 |
| **인프라 비용** | 높음 (VM 많음) | 낮음 |
| **학습 곡선** | 낮음 | 중간 |

---

## 1.5 Docker의 핵심 원리

### 📦 이미지 생성 과정

```
Dockerfile 작성
    ↓
docker build 실행
    ↓
레이어 스택 생성 (캐싱 활용)
    ↓
이미지 저장소에 저장
    ↓
docker run으로 컨테이너 실행
    ↓
컨테이너 내부에서 프로세스 실행
```

### 🔄 컨테이너 라이프사이클

```
Created (생성됨)
    ↓
Running (실행 중)
    ↓
Paused (일시 중지)
    ↓
Stopped (중지됨)
    ↓
Removed (삭제됨)
```

### 📊 레이어 캐싱

```dockerfile
# Dockerfile
FROM python:3.11-slim              # Layer 1: Base Image (캐시됨)
RUN apt-get install git            # Layer 2: 설치 (캐시됨)
COPY requirements.txt .            # Layer 3: 파일 복사
RUN pip install -r requirements.txt # Layer 4: 의존성 설치
COPY ./app .                       # Layer 5: 앱 코드
CMD ["uvicorn", "main:app"]        # Layer 6: 명령

# 코드만 수정 → Layer 5부터 재빌드 (Layer 1-4는 캐시 사용)
# 의존성 수정 → Layer 4부터 재빌드 (Layer 1-3은 캐시 사용)
# 완전히 새 빌드 → 모든 레이어 재생성
```

---

## 1.6 Docker 설치 및 확인

### macOS 설치

```bash
# Docker Desktop 다운로드
# https://www.docker.com/products/docker-desktop

# 또는 Homebrew로 설치
brew install --cask docker

# 설치 확인
docker --version
docker compose version

# Docker 실행 확인
docker ps
```

### Ubuntu/Linux 설치

```bash
# Docker Engine 설치
sudo apt-get update
sudo apt-get install -y docker.io docker-compose

# 설치 확인
docker --version

# 현재 사용자가 docker 그룹 사용 가능하게
sudo usermod -aG docker $USER
newgrp docker

# sudo 없이 사용 가능 확인
docker ps
```

### Windows 설치

```powershell
# Docker Desktop 다운로드
# https://www.docker.com/products/docker-desktop/

# 또는 Chocolatey로 설치
choco install docker-desktop

# PowerShell에서 확인
docker --version
docker compose version
```

---

# 2. 도커 이미지 생성 방법

## 2.1 Dockerfile 기본 구조

### 핵심 명령어 10가지

| 명령어 | 설명 | 예시 |
|--------|------|------|
| **FROM** | 기본 이미지 지정 | `FROM python:3.11-slim` |
| **WORKDIR** | 작업 디렉토리 설정 | `WORKDIR /app` |
| **COPY** | 파일/폴더 복사 | `COPY ./app /app` |
| **ADD** | 파일 복사 + 자동 압축 해제 | `ADD archive.tar.gz /app` |
| **RUN** | 명령 실행 (빌드 시) | `RUN pip install -r req.txt` |
| **ENV** | 환경 변수 설정 | `ENV PYTHONUNBUFFERED=1` |
| **EXPOSE** | 포트 문서화 | `EXPOSE 8000` |
| **CMD** | 기본 실행 명령 | `CMD ["python", "main.py"]` |
| **ENTRYPOINT** | 진입점 (CMD 보다 우선) | `ENTRYPOINT ["uvicorn"]` |
| **USER** | 사용자 설정 | `USER appuser` |

### 간단한 Dockerfile 예제

```dockerfile
# Python FastAPI 앱을 위한 Dockerfile

# 1단계: 기본 이미지 선택
FROM python:3.11-slim

# 2단계: 메타데이터 설정
LABEL maintainer="joohyun@example.com"
LABEL description="FastAPI application"

# 3단계: 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# 4단계: 작업 디렉토리 설정
WORKDIR $APP_HOME

# 5단계: 의존성 파일 복사 (캐싱 최적화)
COPY requirements.txt .

# 6단계: 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 7단계: 앱 코드 복사
COPY ./app .

# 8단계: 포트 노출
EXPOSE 8000

# 9단계: 헬스 체크 (선택사항)
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 10단계: 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 2.2 이미지 빌드 (Build)

### 기본 빌드

```bash
# 현재 디렉토리의 Dockerfile 사용
docker build -t myapp:latest .

# 특정 Dockerfile 지정
docker build -t myapp:latest -f Dockerfile.prod .

# 빌드 태그 (repository:tag)
docker build -t username/myapp:v1.0.0 .
docker build -t localhost:5000/myapp:latest .
```

### 빌드 옵션

```bash
# 캐시 무시 (모든 레이어 재빌드)
docker build --no-cache -t myapp:latest .

# 빌드 변수 전달
docker build --build-arg PYTHON_VERSION=3.11 -t myapp .

# 빌드 진행상황 보기
docker build --progress=plain -t myapp .

# 여러 태그 동시 지정
docker build -t myapp:latest -t myapp:v1.0 .
```

### 빌드 출력 예시

```bash
$ docker build -t myapp:latest .

[+] Building 45.3s (11/11) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 520B
 => [internal] load .dockerignore
 => => transferring context: 2B
 => [1/10] FROM python:3.11-slim
 => => pulling sha256:abc123...
 => => pulling fs layer
 => => downloading 52.2 MB
 => [2/10] WORKDIR /app
 => [3/10] COPY requirements.txt .
 => [4/10] RUN pip install --no-cache-dir -r requirements.txt
 => => running in 5a4b3c2d1e0f
 => [5/10] COPY ./app .
 => [6/10] EXPOSE 8000
 => [7/10] HEALTHCHECK --interval=30s ...
 => [8/10] CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
 => => naming to docker.io/library/myapp:latest
 => => writing image sha256:def456...

✅ 빌드 완료!
```

### 빌드 과정 분석

```bash
# 이미지 레이어 확인
docker history myapp:latest

IMAGE          CREATED       CREATED BY                                      SIZE
def456...      2 minutes ago /bin/sh -c #(nop)  CMD ["uvicorn" "main:app"   0B
abc789...      2 minutes ago /bin/sh -c pip install --no-cache-dir -r req... 120MB
xyz012...      5 minutes ago /bin/sh -c #(nop) COPY file:abc ...             5.3kB
...

# 이미지 상세 정보
docker inspect myapp:latest
```

---

## 2.3 이미지 실행 (Container 생성 및 실행)

### 기본 실행

```bash
# 포그라운드 실행 (터미널 블로킹)
docker run myapp:latest

# 백그라운드 실행 (-d: detached)
docker run -d myapp:latest

# 컨테이너 이름 지정
docker run -d --name my-container myapp:latest

# 컨테이너 중지 및 제거
docker stop my-container
docker rm my-container

# 또는 한 번에
docker run --rm myapp:latest
```

### 포트 매핑

```bash
# 기본: 호스트 포트 → 컨테이너 포트
docker run -d -p 8000:8000 myapp:latest
# localhost:8000 → 컨테이너:8000

# 다른 호스트 포트 사용
docker run -d -p 9000:8000 myapp:latest
# localhost:9000 → 컨테이너:8000

# 특정 IP 바인드
docker run -d -p 127.0.0.1:8000:8000 myapp:latest

# 여러 포트 매핑
docker run -d -p 8000:8000 -p 9000:9000 myapp:latest

# 자동 포트 할당
docker run -d -P myapp:latest
# 사용 가능한 임의의 포트 자동 할당
```

### 환경 변수 전달

```bash
# 단일 환경 변수
docker run -d -e DEBUG=true -e LOG_LEVEL=DEBUG myapp:latest

# .env 파일 사용
docker run -d --env-file .env myapp:latest

# 환경 변수 확인
docker exec my-container printenv
```

### 볼륨 마운트

```bash
# 호스트 디렉토리 마운트 (개발용)
docker run -d -v $(pwd)/app:/app myapp:latest
# 로컬의 app 디렉토리 변경이 컨테이너에 즉시 반영

# 읽기 전용 마운트
docker run -d -v $(pwd)/config:/app/config:ro myapp:latest

# 이름있는 볼륨 (데이터 영속성)
docker run -d -v mydata:/data myapp:latest
# 볼륨은 컨테이너 삭제 후에도 데이터 유지

# 볼륨 확인
docker volume ls
docker volume inspect mydata
```

### 리소스 제한

```bash
# CPU 제한 (2 CPU)
docker run -d --cpus="2" myapp:latest

# 메모리 제한 (1GB)
docker run -d --memory="1g" myapp:latest

# 스왑 메모리 제한
docker run -d --memory="1g" --memory-swap="2g" myapp:latest

# 모두 함께
docker run -d \
  --cpus="2" \
  --memory="1g" \
  --name my-app \
  myapp:latest
```

### 네트워크 설정

```bash
# 기본 네트워크 사용
docker run -d --network bridge myapp:latest

# 호스트 네트워크 사용 (성능 중요시)
docker run -d --network host myapp:latest

# 네트워크 없음
docker run -d --network none myapp:latest

# 커스텀 네트워크 생성 및 사용
docker network create my-network
docker run -d --network my-network --name app1 myapp:latest
docker run -d --network my-network --name app2 myapp:latest
# app1과 app2가 호스트명으로 통신 가능
```

---

## 2.4 Dockerfile 작성 Best Practices

### ❌ 나쁜 예제

```dockerfile
# 문제점 1: 캐싱 무시 (매번 의존성 재설치)
FROM python:3.11
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

# 문제점 2: 큰 기본 이미지 (이미지 크기 1.2GB)
FROM python:3.11

# 문제점 3: 루트 사용자로 실행 (보안 위험)
# USER 선언 안 함

# 문제점 4: 버전 고정 안 함 (재현 불가능)
RUN pip install fastapi
```

### ✅ 좋은 예제

```dockerfile
# 1. 작은 기본 이미지 사용
FROM python:3.11-slim

# 2. 환경 변수로 동작 제어
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 3. 작업 디렉토리 설정
WORKDIR /app

# 4. 의존성 파일만 먼저 복사 (캐싱 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 앱 코드 복사
COPY ./app .

# 6. 비root 사용자 생성 및 사용
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# 7. 포트 노출
EXPOSE 8000

# 8. 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 9. 명시적 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 📋 체크리스트

- [ ] 가장 작은 적합한 기본 이미지 사용 (python:3.11-slim 등)
- [ ] 의존성 파일을 먼저 복사 (코드보다)
- [ ] `--no-cache-dir` 플래그 사용
- [ ] `PYTHONUNBUFFERED=1` 설정
- [ ] 버전 명시 (latest 사용 안 함)
- [ ] 비root 사용자로 실행
- [ ] 헬스 체크 추가
- [ ] 불필요한 파일 제외 (.dockerignore)

---

## 2.5 .dockerignore 파일

`.dockerignore`는 이미지에 포함되지 않을 파일을 지정합니다.

```text
# .dockerignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# 가상 환경
venv/
env/
.venv/

# IDE
.vscode/
.idea/
*.swp

# Git
.git/
.gitignore

# 테스트
.pytest_cache/
.coverage

# 문서
docs/
README.md

# 기타
.env
.env.local
logs/
*.log
```

### 이미지 크기 비교

```bash
# .dockerignore 없음: 500MB
docker build -t myapp:no-ignore .

# .dockerignore 적용: 150MB
docker build -t myapp:with-ignore .

# 약 70% 크기 감소! 🎉
```

---

# 3. 도커 컴포즈 사용 방법

## 3.1 Docker Compose란?

여러 컨테이너를 **YAML 파일**로 정의하고 **한 번의 명령**으로 관리합니다.

### 장점

| 항목 | 설명 |
|------|------|
| **간편성** | 복잡한 docker run 명령을 YAML로 표현 |
| **일괄 관리** | 여러 서비스를 한 번에 시작/중지 |
| **자동 네트워킹** | 서비스 간 통신 자동 구성 |
| **환경 분리** | 개발/테스트/운영 설정 분리 |
| **재현성** | 누구든 같은 환경 구축 가능 |

---

## 3.2 docker-compose.yml 기본 구조

```yaml
# docker-compose.yml

# 버전 (3.8 권장, 최신은 무시됨)
version: '3.8'

# 서비스 정의
services:
  # 서비스 1: FastAPI 앱
  api:
    # 이미지 지정 또는 빌드
    image: myapp:latest
    # 또는
    # build: .
    # build:
    #   context: .
    #   dockerfile: Dockerfile
    
    # 컨테이너 이름
    container_name: my-api
    
    # 포트 매핑
    ports:
      - "8000:8000"
    
    # 환경 변수
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    
    # 볼륨 마운트
    volumes:
      - ./app:/app
      - ./logs:/app/logs
    
    # 의존성
    depends_on:
      - db
    
    # 재시작 정책
    restart: unless-stopped
    
    # 네트워크
    networks:
      - mynetwork

  # 서비스 2: PostgreSQL 데이터베이스
  db:
    image: postgres:15-alpine
    
    container_name: my-db
    
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    
    ports:
      - "5432:5432"
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
    # 헬스 체크
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    
    restart: unless-stopped
    
    networks:
      - mynetwork

# 볼륨 정의
volumes:
  postgres_data:
    driver: local

# 네트워크 정의
networks:
  mynetwork:
    driver: bridge
```

---

## 3.3 Docker Compose 명령어

### 기본 명령어

```bash
# 서비스 시작 (포그라운드)
docker-compose up

# 백그라운드 시작
docker-compose up -d

# 서비스 중지
docker-compose down

# 중지 + 볼륨 삭제
docker-compose down -v

# 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs

# 실시간 로그
docker-compose logs -f

# 특정 서비스 로그만
docker-compose logs -f api
```

### 고급 명령어

```bash
# 이미지 빌드
docker-compose build

# 캐시 무시하고 빌드
docker-compose build --no-cache

# 특정 서비스만 빌드
docker-compose build api

# 이미지 pull
docker-compose pull

# 특정 서비스만 시작
docker-compose up -d api

# 서비스 재시작
docker-compose restart api

# 특정 서비스 재빌드 및 재시작
docker-compose up -d --build api

# 컨테이너 접속
docker-compose exec api bash

# 일회성 명령 실행
docker-compose exec -T db psql -U user -d mydb -c "SELECT * FROM users;"

# 리소스 사용량 확인
docker-compose stats
```

---

## 3.4 환경 변수 관리

### .env 파일 사용

```bash
# .env 파일 생성
cat > .env << EOF
ENVIRONMENT=development
DEBUG=true
API_PORT=8000

POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=mydb
POSTGRES_PORT=5432

REDIS_PORT=6379
EOF
```

### docker-compose.yml에서 .env 참조

```yaml
services:
  api:
    ports:
      - "${API_PORT}:8000"
    environment:
      - ENVIRONMENT=${ENVIRONMENT}
      - DEBUG=${DEBUG}
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:${POSTGRES_PORT}/${POSTGRES_DB}

  db:
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "${POSTGRES_PORT}:5432"
```

### 환경별 설정 분리

```bash
# 개발용 .env.dev
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# 운영용 .env.prod
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
```

```bash
# 개발 환경으로 시작
docker-compose --env-file .env.dev up -d

# 운영 환경으로 시작
docker-compose --env-file .env.prod up -d
```

---

## 3.5 프로필 (Profiles) 활용

### 사용 사례

```yaml
# docker-compose.yml

services:
  api:
    # 항상 실행
    image: myapp:latest

  db:
    # 항상 실행
    image: postgres:15

  pgadmin:
    # dev 프로필에서만 실행
    image: dpage/pgadmin4
    profiles:
      - dev

  redis:
    # cache 프로필에서만 실행
    image: redis:7
    profiles:
      - cache

  monitoring:
    # prod 프로필에서만 실행
    image: prometheus
    profiles:
      - prod
```

### 프로필별 실행

```bash
# 기본: api, db만 시작
docker-compose up -d

# 개발: api, db, pgadmin 시작
docker-compose --profile dev up -d

# 프로덕션: api, db, monitoring 시작
docker-compose --profile prod up -d

# 여러 프로필
docker-compose --profile dev --profile cache up -d
```

---

## 3.6 실전 예제: FastAPI + PostgreSQL + Redis

```yaml
version: '3.8'

services:
  # FastAPI 애플리케이션
  api:
    build: .
    container_name: kaira-api
    ports:
      - "${API_PORT:-8000}:8000"
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=${ENVIRONMENT:-development}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./app:/app/app
    networks:
      - myapp-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # PostgreSQL 데이터베이스
  db:
    image: postgres:15-alpine
    container_name: kaira-db
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-password}
      POSTGRES_DB: ${POSTGRES_DB:-mydb}
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - myapp-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-user}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis 캐시
  redis:
    image: redis:7-alpine
    container_name: kaira-redis
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    networks:
      - myapp-network
    restart: unless-stopped
    command: redis-server --appendonly yes

  # pgAdmin (개발용)
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: kaira-pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: ${PGADMIN_EMAIL:-admin@example.com}
      PGADMIN_DEFAULT_PASSWORD: ${PGADMIN_PASSWORD:-admin}
    ports:
      - "${PGADMIN_PORT:-5050}:80"
    depends_on:
      - db
    networks:
      - myapp-network
    profiles:
      - dev
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  myapp-network:
    driver: bridge
```

### .env 파일

```bash
# 애플리케이션
API_PORT=8000
ENVIRONMENT=development

# PostgreSQL
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydb
DB_PORT=5432

# Redis
REDIS_PORT=6379

# pgAdmin
PGADMIN_EMAIL=admin@example.com
PGADMIN_PASSWORD=admin123
PGADMIN_PORT=5050
```

### 실행

```bash
# 기본 (api, db, redis)
docker-compose up -d

# 개발 모드 (pgadmin 포함)
docker-compose --profile dev up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f api
```

---

# 4. 도커 Build를 사용한 이미지 경량화

## 4.1 이미지 크기가 중요한 이유

```
이미지 크기: 1GB
┌─────────────┐
│ 빌드 시간   │ ↑ 20분 (레지스트리에서 pull 시간)
│ 저장 비용   │ ↑ 스토리지 가격 증가
│ 배포 시간   │ ↑ 대역폭 비용 증가
│ 메모리 사용 │ ↑ 더 많은 컨테이너 실행 불가
│ 부팅 속도   │ ↓ 느림
└─────────────┘

이미지 크기: 100MB (10배 축소)
┌─────────────┐
│ 빌드 시간   │ ↓ 2분
│ 저장 비용   │ ↓ 90% 절감
│ 배포 시간   │ ↓ 빠름
│ 메모리 사용 │ ↓ 더 많은 컨테이너 실행 가능
│ 부팅 속도   │ ↑ 빠름
└─────────────┘
```

---

## 4.2 기본 이미지 선택

### 이미지 크기 비교

```
python:3.11 (full)          1.0 GB  ❌ 불필요
python:3.11-slim            150 MB  ✅ 권장 (일반용)
python:3.11-alpine          50 MB   ✅ 권장 (경량용)
python:3.11-slim-bookworm   170 MB
```

### 선택 기준

| 기본 이미지 | 크기 | 용도 | 호환성 |
|-----------|------|------|--------|
| python:3.11 | 1GB | 완전 호환 필요 시 | ⭐⭐⭐⭐⭐ |
| python:3.11-slim | 150MB | 일반적 경우 | ⭐⭐⭐⭐⭐ |
| python:3.11-alpine | 50MB | 최소 크기 필요 시 | ⭐⭐⭐⭐ |
| ubuntu:22.04 + python | 900MB | 다양한 도구 필요 시 | ⭐⭐⭐ |

### 코드 예제

```dockerfile
# ❌ 나쁜 예: 1GB
FROM python:3.11

# ✅ 좋은 예: 150MB
FROM python:3.11-slim

# ✅ 더 나은 예: 50MB (주의: 일부 바이너리 호환성 문제 가능)
FROM python:3.11-alpine
```

---

## 4.3 멀티 스테이지 빌드 (Multi-Stage Build)

### 개념

여러 단계로 나누어 빌드하고, 최종 단계에만 필요한 파일만 복사합니다.

```
Stage 1 (Builder)          Stage 2 (Runtime)
┌──────────────┐           ┌──────────────┐
│ 빌드 도구    │           │ 필요한 파일  │
│ 컴파일러     │──copy──→  │ 만 포함      │
│ 의존성       │           │              │
│ (불필요)    │           │ 최종 이미지  │
└──────────────┘           └──────────────┘
크기: 500MB              크기: 100MB
                          (80% 감소!)
```

### 멀티 스테이지 Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# === Stage 1: Builder ===
FROM python:3.11-slim AS builder

# 빌드 도구 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Poetry 설치
RUN pip install --no-cache-dir poetry==1.8.5

# 환경 변수 설정
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

# 의존성 파일 복사
COPY pyproject.toml poetry.lock ./

# 의존성 설치 (빌더에만 남음)
RUN poetry install --no-root --only main

# === Stage 2: Runtime (최종 이미지) ===
FROM python:3.11-slim

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Builder에서 설치된 패키지만 복사
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# 앱 코드 복사
COPY ./app .

# 비root 사용자
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 크기 비교

```bash
# 단일 스테이지
docker build -t myapp:single .
# 크기: 500MB (빌드 도구 포함)

# 멀티 스테이지
docker build -t myapp:multi .
# 크기: 100MB (빌드 도구 제외)
# 약 80% 축소! 🎉
```

---

## 4.4 레이어 캐싱 최적화

### ❌ 나쁜 방식 (매번 의존성 재설치)

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 문제: 코드 변경 시 레이어 3,4,5 모두 재빌드
COPY . /app                                      # 레이어 2
RUN pip install -r requirements.txt              # 레이어 3 (시간 오래 걸림)
CMD ["uvicorn", "main:app"]                     # 레이어 4
```

### ✅ 좋은 방식 (의존성은 캐시 사용)

```dockerfile
FROM python:3.11-slim
WORKDIR /app

# 단계 1: 의존성 파일만 복사
COPY requirements.txt .                          # 레이어 2

# 단계 2: 의존성 설치 (변경 빈도 낮음)
RUN pip install --no-cache-dir -r requirements.txt  # 레이어 3

# 단계 3: 코드 복사 (변경 빈도 높음)
COPY ./app .                                     # 레이어 4

CMD ["uvicorn", "main:app"]                     # 레이어 5
```

### 빌드 시간 비교

```bash
# 나쁜 방식
$ docker build -t myapp .
# 첫 빌드: 180초
# 코드 수정 후: 180초 (의존성도 재설치)

# 좋은 방식
$ docker build -t myapp .
# 첫 빌드: 180초
# 코드 수정 후: 10초 (캐시 사용)
# 18배 빠름! 🚀
```

---

## 4.5 불필요한 파일 제외

### .dockerignore 최적화

```text
# Python
__pycache__/
*.py[cod]
.Python
*.egg-info/
dist/
build/
.eggs/

# Virtual environments
venv/
env/
.venv/

# Testing & Coverage
.pytest_cache/
.coverage
htmlcov/

# IDE & Editor
.vscode/
.idea/
*.swp
*.swo
*~

# Version Control
.git/
.gitignore

# Documentation
docs/
README.md

# Development
.env.local
.env.*.local
.DS_Store

# Logs
logs/
*.log

# Database
*.db
*.sqlite

# Node modules (프론트엔드)
node_modules/
npm-debug.log
```

### 효과

```bash
# .dockerignore 없음
docker build -t myapp .
# 이미지 크기: 500MB

# .dockerignore 적용
docker build -t myapp .
# 이미지 크기: 200MB
# 60% 축소! 📦
```

---

## 4.6 고급 최적화 기법

### 1️⃣ 명령어 통합

```dockerfile
# ❌ 나쁜 예 (3개 레이어)
RUN apt-get update
RUN apt-get install -y git curl
RUN rm -rf /var/lib/apt/lists/*

# ✅ 좋은 예 (1개 레이어)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*
```

### 2️⃣ --no-install-recommends 사용

```dockerfile
# ❌ 나쁜 예: 불필요한 패키지도 설치
RUN apt-get install -y git

# ✅ 좋은 예: 필수 패키지만 설치
RUN apt-get install -y --no-install-recommends git
```

### 3️⃣ 캐시 비활성화

```dockerfile
# ❌ 나쁜 예: 캐시로 인해 구버전 패키지 사용
RUN apt-get install -y curl

# ✅ 좋은 예: 최신 버전 설치
RUN apt-get update && apt-get install -y curl
```

### 4️⃣ 파일 정리

```dockerfile
# ❌ 큰 파일 설치 후 미정리
RUN apt-get install -y git  # 100MB

# ✅ 설치 후 즉시 정리
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*  # 50MB
```

### 5️⃣ 변수 사용으로 유지보수성 향상

```dockerfile
# 버전을 상단에 정의
ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.8.5

FROM python:${PYTHON_VERSION}-slim

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}
```

---

## 4.7 최적화 종합 예제

```dockerfile
# syntax=docker/dockerfile:1

# 빌드 인자
ARG PYTHON_VERSION=3.11
ARG POETRY_VERSION=1.8.5

# === Stage 1: Dependencies ===
FROM python:${PYTHON_VERSION}-slim AS dependencies

ARG POETRY_VERSION

# 최소한의 빌드 도구만 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /build

# Poetry 설정
ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_NO_ANSI=1

# 의존성 파일만 복사 (캐싱 최적화)
COPY pyproject.toml poetry.lock ./

# 프로덕션 의존성만 설치
RUN poetry install --no-root --only main

# === Stage 2: Runtime ===
FROM python:${PYTHON_VERSION}-slim

# 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production

WORKDIR /app

# 의존성 복사
COPY --from=dependencies /usr/local/lib/python${PYTHON_VERSION}/site-packages \
    /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=dependencies /usr/local/bin /usr/local/bin

# 앱 코드 복사
COPY ./app .

# 비root 사용자
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 포트 노출
EXPOSE 8000

# 헬스 체크
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 실행
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 최적화 결과

| 항목 | 이전 | 이후 | 개선 |
|------|------|------|------|
| 이미지 크기 | 800MB | 150MB | **81% 축소** |
| 빌드 시간 | 240초 | 180초 | **25% 단축** |
| 코드 수정 후 빌드 | 240초 | 15초 | **94% 단축** |
| 배포 시간 | 90초 | 10초 | **89% 단축** |

---

## 4.8 이미지 크기 분석 도구

### 1️⃣ docker history

```bash
# 각 레이어 크기 확인
docker history myapp:latest

IMAGE          CREATED        SIZE
abc123...      2 hours ago    0B     # CMD
def456...      2 hours ago    5MB    # COPY ./app
ghi789...      2 hours ago    120MB  # RUN pip install
jkl012...      3 hours ago    0B     # WORKDIR
mno345...      3 hours ago    150MB  # FROM python:3.11-slim
```

### 2️⃣ dive (분석 도구)

```bash
# 설치
brew install dive

# 분석
dive myapp:latest

# 대화형 UI에서 각 레이어 상세 분석 가능
```

### 3️⃣ buildkit 상세 분석

```bash
# BuildKit 상세 정보와 함께 빌드
DOCKER_BUILDKIT=1 docker build -t myapp:latest . --progress=plain

# BuildKit을 사용한 빌드 (더 효율적)
docker buildx build -t myapp:latest .
```

---

## 4.9 체크리스트: 이미지 경량화

배포 전 다음을 확인하세요:

### 기본 이미지
- [ ] python:3.11-slim 또는 alpine 사용
- [ ] latest 태그 대신 명시적 버전 지정

### 멀티 스테이지 빌드
- [ ] Builder와 Runtime 단계 분리
- [ ] Builder 도구가 최종 이미지에 포함되지 않음

### 레이어 최적화
- [ ] 의존성 파일을 먼저 복사
- [ ] 코드는 나중에 복사
- [ ] 명령어 통합 (&&로)

### 불필요한 파일 제외
- [ ] .dockerignore 파일 생성
- [ ] __pycache__, .git 등 제외

### 캐시 최적화
- [ ] --no-cache-dir 플래그 사용
- [ ] apt-get 후 정리

### 보안 & 성능
- [ ] 비root 사용자로 실행
- [ ] 헬스 체크 추가
- [ ] 환경 변수 설정

### 최종 확인
- [ ] `docker history` 로 레이어 확인
- [ ] 이미지 크기 < 300MB
- [ ] 빌드 시간 < 3분

---

# 📚 부록: 자주 사용되는 명령어 모음

## Docker 기본 명령어

```bash
# 이미지
docker images                          # 이미지 목록
docker build -t myapp:latest .         # 이미지 빌드
docker tag myapp:latest username/myapp:latest  # 태그 지정
docker push username/myapp:latest      # 푸시
docker pull username/myapp:latest      # 풀
docker rmi IMAGE_ID                    # 삭제
docker inspect IMAGE_ID                # 상세 정보

# 컨테이너
docker ps                              # 실행 중인 컨테이너
docker ps -a                           # 모든 컨테이너
docker run -d -p 8000:8000 myapp:latest  # 실행
docker stop CONTAINER_ID               # 중지
docker start CONTAINER_ID              # 시작
docker restart CONTAINER_ID            # 재시작
docker rm CONTAINER_ID                 # 삭제
docker logs CONTAINER_ID               # 로그
docker exec -it CONTAINER bash         # 접속

# 시스템
docker system df                       # 디스크 사용량
docker system prune -a                 # 불필요한 리소스 삭제
docker stats                           # 리소스 사용량
```

## Docker Compose 명령어

```bash
# 시작/중지
docker-compose up                      # 시작
docker-compose up -d                   # 백그라운드
docker-compose down                    # 중지
docker-compose down -v                 # 중지 + 볼륨 삭제

# 관리
docker-compose ps                      # 상태
docker-compose logs -f                 # 로그
docker-compose restart api             # 재시작
docker-compose build                   # 빌드
docker-compose pull                    # 풀

# 운영
docker-compose exec api bash           # 접속
docker-compose exec db psql -U user    # DB 접근
```

---

**작성일**: 2025-11-11  
**대상**: FastAPI 개발자  
**버전**: Docker 27.x, docker-compose 2.x

