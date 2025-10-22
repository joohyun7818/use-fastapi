# 06. 클라우드 배포 완벽 가이드

> FastAPI 애플리케이션을 클라우드 플랫폼에 배포하고 프로덕션 환경을 구성하는 방법을 배웁니다.

## 📚 6단계 목차

| 챕터 | 주제 | 예상 시간 |
|------|------|---------|
| [6.1](#61-배포-옵션-비교) | 배포 옵션 비교 | 30분 |
| [6.2](#62-aws-ec2-배포-aws-ec2-배포) | AWS EC2 배포 | 2시간 |
| [6.3](#63-gcp-app-engine-대안) | GCP App Engine 대안 | 1시간 |
| [6.4](#64-도메인-연결) | 도메인 연결 | 30분 |
| [6.5](#65-ssl-인증서-설정) | SSL 인증서 설정 | 45분 |
| [6.6](#66-cicd-자동화) | CI/CD 자동화 | 1시간 30분 |
| [6.7](#67-모니터링과-로깅) | 모니터링과 로깅 | 1시간 |
| [6.8](#68-문제-해결) | 문제 해결 | 30분 |
| [6.9](#69-체크리스트) | 체크리스트 | - |

---

## 6.1 배포 옵션 비교

### 6.1.1 주요 옵션

| 옵션 | 난이도 | 비용 | 확장성 | 추천 상황 |
|------|--------|------|--------|-----------|
| **AWS EC2** | 중간 | 낮음 | 높음 | 완전한 제어 필요, 초보자 학습 |
| **GCP App Engine** | 쉬움 | 중간 | 자동 | 빠른 배포, 관리 최소화 |
| **Heroku** | 매우 쉬움 | 높음 | 중간 | 프로토타입, 취미 프로젝트 |
| **Digital Ocean** | 쉬움 | 낮음 | 중간 | 간단한 설정, 고정 비용 |
| **Vercel/Railway** | 매우 쉬움 | 낮음 | 자동 | 무료 티어, 취미 프로젝트 |

### 6.1.2 이 가이드의 선택

우리는 **AWS EC2**를 메인으로 다룹니다. 이유는:

1. **학습 가치**: 클라우드 인프라의 기본을 배울 수 있음
2. **유연성**: 모든 것을 직접 제어 가능
3. **확장성**: 나중에 로드 밸런서, 오토 스케일링 등 추가 가능
4. **비용**: 프리 티어로 1년간 무료 사용 가능
5. **취업 시장**: AWS 경험이 가장 많이 요구됨

**GCP App Engine**도 간단히 다루어 비교할 수 있게 합니다.

---

## 6.2 AWS EC2 배포 AWS EC2 배포

### 6.2.1 AWS 계정 생성

1. **AWS 회원가입**:
   - https://aws.amazon.com/ko/
   - "무료 계정 생성" 클릭
   - 이메일, 비밀번호 입력
   - **중요**: 신용카드 등록 필요 (프리 티어는 무료)

2. **프리 티어 확인**:
   - t2.micro/t3.micro 인스턴스
   - 월 750시간 무료 (24시간 × 31일 = 744시간)
   - 30GB EBS 스토리지
   - 1년간 무료

3. **IAM 사용자 생성 (권장)**:
   ```
   1. AWS Console → IAM → Users → Add users
   2. 이름: fastapi-deploy
   3. Access type: Programmatic access + Console access
   4. Permissions: AdministratorAccess (학습용, 실제 운영은 최소 권한)
   5. Create user
   6. Access Key ID와 Secret Access Key 저장 (다시 볼 수 없음!)
   ```

### 6.2.2 EC2 인스턴스 생성

**AWS Console에서**:

1. **EC2 Dashboard로 이동**:
   - Services → EC2 → Launch Instance

2. **인스턴스 설정**:
   ```
   이름: kaira-fastapi-server

   Application and OS Images (AMI):
   - Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
   - 64-bit (x86)

   Instance type:
   - t2.micro (프리 티어)
   - t3.micro (더 빠름, 프리 티어 가능)

   Key pair (로그인):
   - Create new key pair
   - 이름: kaira-key
   - 타입: RSA
   - 형식: .pem (macOS/Linux) 또는 .ppk (Windows PuTTY)
   - Download key pair (저장 필수!)
   ```

3. **네트워크 설정**:
   ```
   Security Group (방화벽):
   - SSH: 포트 22, 소스: My IP (보안을 위해 내 IP만 허용)
   - HTTP: 포트 80, 소스: Anywhere (0.0.0.0/0)
   - HTTPS: 포트 443, 소스: Anywhere (0.0.0.0/0)
   - Custom TCP: 포트 8000, 소스: Anywhere (개발 테스트용, 나중에 제거)
   ```

4. **스토리지 설정**:
   ```
   1 x 30 GiB gp3 (프리 티어)
   ```

5. **Launch instance** 클릭

### 6.2.3 SSH 접속

**macOS/Linux**:
```bash
# 키 파일 권한 변경 (필수!)
chmod 400 ~/Downloads/kaira-key.pem

# EC2 인스턴스에 접속
ssh -i ~/Downloads/kaira-key.pem ubuntu@<EC2_PUBLIC_IP>

# 예시
ssh -i ~/Downloads/kaira-key.pem ubuntu@13.125.123.45
```

**Windows (PowerShell)**:
```powershell
# Git Bash 또는 WSL 사용 권장
ssh -i C:\Users\YourName\Downloads\kaira-key.pem ubuntu@<EC2_PUBLIC_IP>
```

**접속 성공 시**:
```
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 6.2.0-1009-aws x86_64)
ubuntu@ip-172-31-0-123:~$
```

### 6.2.4 서버 초기 설정

```bash
# 패키지 업데이트
sudo apt-get update
sudo apt-get upgrade -y

# 필수 도구 설치
sudo apt-get install -y curl wget git vim

# Docker 설치
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 현재 사용자를 docker 그룹에 추가
sudo usermod -aG docker $USER

# docker-compose 설치
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 재접속 (docker 그룹 권한 적용)
exit
ssh -i ~/Downloads/kaira-key.pem ubuntu@<EC2_PUBLIC_IP>

# 설치 확인
docker --version
docker-compose --version
```

### 6.2.5 코드 배포

**방법 1: Git Clone (권장)**:
```bash
# Git 저장소 클론
cd ~
git clone https://github.com/yourusername/kaira-fastapi.git
cd kaira-fastapi

# 환경 변수 설정
cp .env.example .env
vim .env
# ENVIRONMENT=production
# DEBUG=false 등 설정

# Docker 이미지 빌드
docker build -t kaira-server -f Dockerfile.prod .

# 컨테이너 실행
docker run -d -p 80:80 --name kaira-server --restart unless-stopped kaira-server

# 실행 확인
docker ps
curl http://localhost
```

**방법 2: docker-compose (더 간편)**:
```bash
# docker-compose로 실행
docker-compose -f docker-compose.prod.yml up -d

# 로그 확인
docker-compose -f docker-compose.prod.yml logs -f

# 중지
docker-compose -f docker-compose.prod.yml down
```

**방법 3: Docker Hub 활용**:
```bash
# 로컬에서 빌드 후 푸시
docker build -t yourusername/kaira-server:latest -f Dockerfile.prod .
docker login
docker push yourusername/kaira-server:latest

# EC2에서 풀 받아서 실행
ssh ubuntu@<EC2_PUBLIC_IP>
docker pull yourusername/kaira-server:latest
docker run -d -p 80:80 --restart unless-stopped yourusername/kaira-server:latest
```

### 6.2.6 접속 확인

```bash
# EC2 Public IP로 접속
curl http://<EC2_PUBLIC_IP>

# 또는 브라우저에서
# http://<EC2_PUBLIC_IP>
```

---

## 6.3 GCP App Engine 대안

### 6.4.1 GCP App Engine 특징

**장점**:
- ✅ 자동 스케일링
- ✅ 로드 밸런싱 자동
- ✅ HTTPS 자동 설정
- ✅ 관리 불필요 (서버리스)

**단점**:
- ❌ EC2보다 비용 높을 수 있음
- ❌ 제한된 커스터마이징
- ❌ 특정 런타임만 지원

### 6.4.2 app.yaml 작성

```yaml
# app.yaml
runtime: python311

instance_class: F1  # 프리 티어

env_variables:
  ENVIRONMENT: "production"
  DEBUG: "false"

entrypoint: uvicorn kaira_fastapi_poetry.main:app --host 0.0.0.0 --port $PORT

automatic_scaling:
  min_instances: 0
  max_instances: 2
  target_cpu_utilization: 0.65

handlers:
- url: /static
  static_dir: kaira-1.0.0
  secure: always

- url: /.*
  script: auto
  secure: always
```

### 6.4.3 배포 방법

```bash
# Google Cloud SDK 설치
curl https://sdk.cloud.google.com | bash

# 초기화
gcloud init

# 프로젝트 생성
gcloud projects create kaira-fastapi --name="Kaira FastAPI"

# App Engine 앱 생성
gcloud app create --project=kaira-fastapi --region=asia-northeast3

# 배포
gcloud app deploy

# 확인
gcloud app browse
```

---

## 6.4 도메인 연결

### 6.5.1 도메인 구매

**도메인 등록 업체**:
- **국내**: Gabia, Whois, Cafe24
- **해외**: Namecheap, GoDaddy, Google Domains

**추천 도메인**:
- `.com` / `.net` (국제적)
- `.co.kr` (한국)
- `.io` (개발자 친화적)

**비용**: 연간 1만~3만원

### 6.5.2 DNS 설정

**예: Gabia에서 구매한 경우**:

1. **Gabia 로그인** → My가비아 → 도메인 관리

2. **DNS 설정**:
   ```
   레코드 타입: A
   호스트: @ (또는 빈칸)
   값/위치: <EC2_PUBLIC_IP>
   TTL: 3600

   레코드 타입: A
   호스트: www
   값/위치: <EC2_PUBLIC_IP>
   TTL: 3600
   ```

3. **전파 대기** (최대 48시간, 보통 1~2시간):
   ```bash
   # DNS 전파 확인
   nslookup yourdomain.com
   dig yourdomain.com
   ```

### 6.5.3 Elastic IP 사용 (권장)

EC2의 Public IP는 재시작 시 변경됩니다. **Elastic IP**로 고정하세요:

```
1. AWS Console → EC2 → Elastic IPs
2. Allocate Elastic IP address
3. Actions → Associate Elastic IP address
4. Instance: 선택
5. Associate
```

이제 DNS에 Elastic IP를 설정하면 영구적으로 사용 가능합니다.

---

## 6.5 SSL 인증서 설정

### 6.6.1 Certbot으로 Let's Encrypt 인증서 발급

**EC2 서버에서**:

```bash
# Certbot 설치
sudo apt-get update
sudo apt-get install -y certbot python3-certbot-nginx

# Nginx 설치 (아직 안 했다면)
sudo apt-get install -y nginx

# Nginx 기본 설정
sudo vim /etc/nginx/sites-available/default
```

**Nginx 기본 설정** (`/etc/nginx/sites-available/default`):
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/kaira-fastapi/kaira-1.0.0/;
    }
}
```

**Nginx 재시작**:
```bash
sudo nginx -t  # 설정 테스트
sudo systemctl restart nginx
```

**Certbot으로 SSL 인증서 발급**:
```bash
# 자동 설정
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# 이메일 입력: your-email@example.com
# 약관 동의: Y
# HTTPS 리다이렉트: 2 (권장)
```

**완료 시**:
```
Congratulations! You have successfully enabled https://yourdomain.com
```

### 6.6.2 자동 갱신 설정

Let's Encrypt 인증서는 90일마다 갱신해야 합니다.

```bash
# 자동 갱신 테스트
sudo certbot renew --dry-run

# 자동 갱신 Cron 작업 (이미 설정됨)
sudo crontab -l

# 수동 갱신 (필요 시)
sudo certbot renew
```

### 6.6.3 최종 Nginx 설정 확인

Certbot이 자동으로 수정한 설정:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;  # HTTP → HTTPS 리다이렉트
}

server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/ubuntu/kaira-fastapi/kaira-1.0.0/;
    }
}
```

**접속 확인**:
```bash
# HTTPS로 접속
curl https://yourdomain.com
```

---

## 6.6 CI/CD 자동화

### 6.7.1 GitHub Actions 워크플로우

**.github/workflows/deploy.yml**:
```yaml
name: Deploy to AWS EC2

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: |
          poetry run pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to EC2
        env:
          SSH_PRIVATE_KEY: ${{ secrets.EC2_SSH_KEY }}
          EC2_HOST: ${{ secrets.EC2_HOST }}
          EC2_USER: ubuntu
        run: |
          # SSH 키 설정
          echo "$SSH_PRIVATE_KEY" > private_key.pem
          chmod 600 private_key.pem

          # EC2에 배포
          ssh -o StrictHostKeyChecking=no -i private_key.pem ${EC2_USER}@${EC2_HOST} << 'EOF'
            cd kaira-fastapi
            git pull origin main
            docker-compose -f docker-compose.prod.yml down
            docker-compose -f docker-compose.prod.yml build
            docker-compose -f docker-compose.prod.yml up -d
          EOF
```

### 6.7.2 GitHub Secrets 설정

```
1. GitHub Repository → Settings → Secrets and variables → Actions
2. New repository secret:
   - Name: EC2_SSH_KEY
   - Value: (kaira-key.pem 파일 내용)

3. New repository secret:
   - Name: EC2_HOST
   - Value: <EC2_PUBLIC_IP>
```

### 6.7.3 무중단 배포 (Blue-Green)

**docker-compose.blue-green.yml**:
```yaml
version: '3.8'

services:
  app-blue:
    build: .
    container_name: kaira-blue
    ports:
      - "8001:80"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped

  app-green:
    build: .
    container_name: kaira-green
    ports:
      - "8002:80"
    environment:
      - ENVIRONMENT=production
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: kaira-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx-blue-green.conf:/etc/nginx/nginx.conf
    depends_on:
      - app-blue
      - app-green
```

**배포 스크립트** (`deploy-blue-green.sh`):
```bash
#!/bin/bash

# 현재 활성 컨테이너 확인
ACTIVE=$(docker ps --filter "name=kaira-blue" --filter "status=running" --format "{{.Names}}")

if [ "$ACTIVE" = "kaira-blue" ]; then
    INACTIVE="green"
    INACTIVE_PORT=8002
else
    INACTIVE="blue"
    INACTIVE_PORT=8001
fi

echo "현재 활성: ${ACTIVE:-green}"
echo "배포 대상: kaira-$INACTIVE"

# Inactive 컨테이너 업데이트
docker-compose -f docker-compose.blue-green.yml build app-$INACTIVE
docker-compose -f docker-compose.blue-green.yml up -d app-$INACTIVE

# 헬스 체크
sleep 5
if curl -f http://localhost:$INACTIVE_PORT/health; then
    echo "헬스 체크 성공"
    # Nginx 설정 전환
    sed -i "s/kaira-[^:]*:80/kaira-$INACTIVE:80/" nginx-blue-green.conf
    docker exec kaira-nginx nginx -s reload
    echo "배포 완료: kaira-$INACTIVE"
else
    echo "헬스 체크 실패, 롤백"
    exit 1
fi
```

---

## 6.7 모니터링과 로깅

### 6.8.1 CloudWatch 로그 설정 (AWS)

**CloudWatch Logs Agent 설치**:
```bash
# EC2에서
sudo apt-get install -y awslogs

# 설정 파일 편집
sudo vim /etc/awslogs/awslogs.conf
```

**awslogs.conf**:
```ini
[/var/log/docker/kaira.log]
datetime_format = %Y-%m-%d %H:%M:%S
file = /var/log/docker/kaira.log
buffer_duration = 5000
log_stream_name = {instance_id}
initial_position = start_of_file
log_group_name = /aws/ec2/kaira-fastapi
```

**Docker 로그 파일로 출력**:
```bash
# docker-compose.prod.yml에 추가
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### 6.8.2 Prometheus + Grafana (고급)

**docker-compose.monitoring.yml**:
```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  prometheus_data:
  grafana_data:
```

**prometheus.yml**:
```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['app:80']
```

**FastAPI에 Prometheus 메트릭 추가**:
```bash
poetry add prometheus-fastapi-instrumentator
```

```python
# app/main.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

# Prometheus 메트릭 추가
Instrumentator().instrument(app).expose(app)
```

### 6.8.3 알람 설정

**AWS CloudWatch Alarm**:
```
1. CloudWatch → Alarms → Create Alarm
2. Metric: EC2 → Per-Instance Metrics → CPUUtilization
3. Threshold: Greater than 80%
4. Notification: SNS Topic (이메일 또는 SMS)
```

**Uptime 모니터링 (무료)**:
- **UptimeRobot**: https://uptimerobot.com/
- **Pingdom**: https://www.pingdom.com/
- **StatusCake**: https://www.statuscake.com/

설정:
```
1. 회원가입
2. Add New Monitor
3. URL: https://yourdomain.com/health
4. Interval: 5 minutes
5. Alert Contacts: 이메일
```

---

## 6.8 문제 해결

### 6.9.1 자주 발생하는 문제

#### 문제 1: 도메인 접속 안 됨

**증상**:
```
This site can't be reached
```

**해결**:
```bash
# 1. DNS 전파 확인
nslookup yourdomain.com

# 2. Security Group 확인
# AWS Console → EC2 → Security Groups
# HTTP (80), HTTPS (443) 포트 열렸는지 확인

# 3. Nginx 상태 확인
sudo systemctl status nginx

# 4. 방화벽 확인
sudo ufw status
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

#### 문제 2: SSL 인증서 발급 실패

**증상**:
```
Failed to obtain a certificate from the CA
```

**해결**:
```bash
# 1. DNS가 올바르게 설정되었는지 확인
dig yourdomain.com

# 2. 80번 포트가 열려 있는지 확인
sudo netstat -tulpn | grep :80

# 3. Certbot 재시도
sudo certbot --nginx -d yourdomain.com --debug
```

#### 문제 3: Docker 컨테이너 재시작 안 됨

**증상**:
```
Container exited (1)
```

**해결**:
```bash
# 1. 로그 확인
docker logs kaira-server

# 2. 환경 변수 확인
docker exec kaira-server env

# 3. 재시작 정책 확인
docker inspect kaira-server | grep -i restart
```

### 6.9.2 성능 문제

**느린 응답 시간**:
```bash
# 1. 서버 리소스 확인
top
htop
docker stats

# 2. Uvicorn worker 증가
# docker-compose.prod.yml
CMD ["uvicorn", "app.main:app", "--workers", "4"]

# 3. Nginx 캐싱 설정
# nginx.conf에 추가
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m;
location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 1h;
}
```

**메모리 부족**:
```bash
# 스왑 메모리 추가
sudo fallocate -l 1G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# 영구 설정
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 6.9 체크리스트

프로젝트에 다음 항목들이 구현되었는지 확인하세요:

### AWS EC2 배포

- [ ] AWS 계정 생성 및 프리 티어 확인
- [ ] EC2 인스턴스 생성 (t2.micro/t3.micro)
- [ ] Security Group 설정 (SSH, HTTP, HTTPS)
- [ ] SSH 키 다운로드 및 접속 성공
- [ ] Docker 설치 및 확인
- [ ] 코드 배포 (Git Clone 또는 Docker Hub)
- [ ] 컨테이너 실행 및 접속 확인

### 도메인 및 SSL

- [ ] 도메인 구매
- [ ] DNS A 레코드 설정
- [ ] Elastic IP 할당 (권장)
- [ ] DNS 전파 확인
- [ ] Nginx 설치 및 설정
- [ ] Let's Encrypt SSL 인증서 발급
- [ ] HTTPS 강제 리다이렉트 설정
- [ ] SSL 자동 갱신 확인

### CI/CD

- [ ] GitHub Actions 워크플로우 작성
- [ ] GitHub Secrets 설정
- [ ] 푸시 시 자동 배포 테스트
- [ ] 무중단 배포 전략 (선택사항)

### 모니터링

- [ ] 헬스 체크 엔드포인트 추가
- [ ] CloudWatch 로그 설정 (AWS)
- [ ] Uptime 모니터링 설정
- [ ] 알람 설정 (CPU, 메모리, Uptime)
- [ ] Prometheus + Grafana (선택사항)

### 프로덕션 설정

- [ ] 로그 로테이션 설정
- [ ] 자동 재시작 설정 (--restart unless-stopped)
- [ ] 환경 변수 프로덕션 설정
- [ ] 방화벽 설정 (불필요한 포트 차단)
- [ ] 백업 계획 수립

### 문서화

- [ ] 배포 절차 문서화
- [ ] 트러블슈팅 가이드 작성
- [ ] 인프라 다이어그램 작성
- [ ] 비용 예상 문서화

---

## 📚 최종 완료!

축하합니다! 5단계를 모두 완료했습니다! 🎉

### 당신이 달성한 것

1. **1단계**: FastAPI 기초와 정적 파일 서빙
2. **2단계**: Poetry로 의존성 관리
3. **3단계**: pytest로 테스트, 로깅, 환경 변수 관리
4. **4단계**: Docker로 컨테이너화
5. **5단계**: AWS EC2에 프로덕션 배포, 도메인 연결, SSL 설정

### 다음 학습 경로

**심화 학습**:
- 데이터베이스 통합 (PostgreSQL, MongoDB)
- 인증/인가 (OAuth2, JWT)
- 캐싱 (Redis)
- 메시지 큐 (Celery, RabbitMQ)
- WebSocket 실시간 통신
- GraphQL API
- Kubernetes 오케스트레이션

**운영 개선**:
- Auto Scaling
- 로드 밸런서 (AWS ALB)
- CDN (CloudFront)
- 로그 집계 (ELK Stack)
- APM (Application Performance Monitoring)

**비용 최적화**:
- Reserved Instances
- Spot Instances
- CloudWatch Budget Alerts

---

## 🎯 핵심 요약

이번 단계에서 배운 내용:

1. **AWS EC2**: 클라우드 인스턴스 생성 및 관리
2. **도메인 연결**: DNS 설정, Elastic IP
3. **SSL 인증서**: Let's Encrypt, HTTPS 강제
4. **CI/CD**: GitHub Actions 자동 배포
5. **모니터링**: CloudWatch, Uptime 모니터링

**최종 아키텍처**:
```
[사용자] → [도메인] → [Route 53/DNS]
                           ↓
               [Elastic IP] → [EC2 인스턴스]
                           ↓
                      [Nginx (SSL)]
                           ↓
               [Docker Container (FastAPI)]
                           ↓
                  [정적 파일 / API]
```

**핵심 명령어**:
```bash
# SSH 접속
ssh -i key.pem ubuntu@<EC2_IP>

# Docker 실행
docker-compose -f docker-compose.prod.yml up -d

# SSL 발급
sudo certbot --nginx -d yourdomain.com

# 배포
git pull && docker-compose -f docker-compose.prod.yml up -d --build
```

이제 당신은 FastAPI 애플리케이션을 처음부터 끝까지 완성하고 배포할 수 있습니다! 🚀

---

**작성일**: 2025-01-XX  
**최종 검증**: AWS EC2 (Ubuntu 22.04), FastAPI 0.115.x, Docker 27.x

**참고 문서**:
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [GitHub Actions](https://docs.github.com/en/actions)
