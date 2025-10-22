# FastAPI 학습 완전 가이드: CLI → Poetry → 클라우드 배포

> **이 가이드는 당신의 정적 웹사이트를 FastAPI로 서빙하고, 클라우드 인스턴스에 배포하기까지의 완전한 학습 경로입니다.**

---

## 📚 학습 구조

이 가이드는 **5단계의 순차적 튜토리얼**로 구성되어 있습니다.

각 단계는 **독립적인 문서**이면서도, **연속적으로 진행**되도록 설계되었습니다.

### 전체 흐름

```
┌──────────────────────────────────────────────────────────────┐
│                    1단계: FastAPI-CLI                         │
│           빠른 프로토타입으로 기초 학습 (2-3일)              │
│                                                               │
│   학습: 라우팅, 엔드포인트, 정적 파일 서빙                  │
│   결과: http://127.0.0.1:8000 에서 앱 실행                  │
└──────────────────────────────────────────────────────────────┘
                          ⬇️
┌──────────────────────────────────────────────────────────────┐
│                    2단계: Poetry 재구성                       │
│        같은 프로젝트를 의존성 관리로 재구성 (2-3일)          │
│                                                               │
│   학습: 의존성 관리, 가상환경, 프로젝트 구조                │
│   결과: Poetry로 관리하는 프로덕션 구조 완성                │
└──────────────────────────────────────────────────────────────┘
                          ⬇️
┌──────────────────────────────────────────────────────────────┐
│               3단계: 테스트와 로깅                           │
│         신뢰할 수 있는 코드 작성 (3-5일)                     │
│                                                               │
│   학습: pytest, TestClient, 에러 처리, 로깅, 환경변수     │
│   결과: 테스트가 완비된 프로덕션급 코드                    │
└──────────────────────────────────────────────────────────────┘
                          ⬇️
┌──────────────────────────────────────────────────────────────┐
│             4단계: 데이터베이스 연결 및 관리                 │
│       SQLAlchemy로 데이터 다루기 (5-7일)                    │
│                                                               │
│   학습: SQLAlchemy, PostgreSQL, CRUD, 마이그레이션         │
│   결과: 데이터베이스 기능을 갖춘 프로덕션 앱              │
└──────────────────────────────────────────────────────────────┘
                          ⬇️
┌──────────────────────────────────────────────────────────────┐
│                5단계: Docker 컨테이너화                      │
│         어디서나 동일하게 실행 (2-3일)                      │
│                                                               │
│   학습: Dockerfile, 이미지 빌드, docker-compose            │
│   결과: Docker 컨테이너로 앱 배포 가능                     │
└──────────────────────────────────────────────────────────────┘
                          ⬇️
┌──────────────────────────────────────────────────────────────┐
│              6단계: 클라우드 배포 (AWS/GCP)                 │
│         실제 서비스 운영 (3-5일)                            │
│                                                               │
│   학습: EC2/App Engine, 도메인, SSL, 모니터링              │
│   결과: 공개 URL에서 앱 서비스 중                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 📖 각 단계별 가이드

### 🎯 1단계: FastAPI로 빠른 프로토타입 만들기

**파일**: [`01_FASTAPI_CLI_GUIDE.md`](./01_FASTAPI_CLI_GUIDE.md)

**목표**:
- FastAPI 기초 개념 이해
- 로컬 개발 서버 구동
- 정적 파일 서빙
- API 문서 자동 생성

**학습 시간**: 2-3일
**난이도**: ⭐ (쉬움)

**이 단계에서 배울 것**:
- FastAPI와 Uvicorn 설치
- 수동으로 프로젝트 폴더 생성
- 라우팅 (`@app.get()`, `@app.post()` 등)
- 경로 매개변수 (`/items/{item_id}`)
- 정적 파일 마운트 (`StaticFiles`)
- Swagger UI/ReDoc 활용

**완료 시나리오**:
```bash
uvicorn main:app --reload
# http://127.0.0.1:8000 에서 API 실행
# http://127.0.0.1:8000/docs 에서 Swagger 문서 확인
```

---

### 🎯 2단계: Poetry로 프로덕션 구조 재구성

**파일**: [`02_POETRY_GUIDE.md`](./02_POETRY_GUIDE.md)

**목표**:
- 같은 프로젝트를 Poetry로 재구성
- 의존성 관리 방법 학습
- 프로덕션급 폴더 구조 설계

**학습 시간**: 3-4시간
**난이도**: ⭐⭐ (중간)

**이 단계에서 배울 것**:
- Poetry 설치 및 프로젝트 초기화
- `poetry add` 로 의존성 추가
- `pyproject.toml` 파일 이해
- 가상환경 관리 (`poetry shell`)
- 개발/프로덕션 의존성 분리
- 패키지 구조 설계 (app/, tests/, config/)

**완료 시나리오**:
```bash
poetry shell
poetry run uvicorn kaira_fastapi_poetry.main:app --reload
# http://127.0.0.1:8000 에서 Poetry 프로젝트 실행
# 의존성 자동 관리, 가상환경 분리 완료
```

---

### 🎯 3단계: 테스트와 로깅 완벽 가이드

**파일**: [`03_TESTING_LOGGING_GUIDE.md`](./03_TESTING_LOGGING_GUIDE.md)

**목표**:
- pytest로 체계적인 테스트 작성
- FastAPI TestClient 활용
- 에러 처리 및 로깅 시스템 구축
- 환경 변수 관리 (pydantic-settings)

**학습 시간**: 4-6시간
**난이도**: ⭐⭐ (중간)

**이 단계에서 배울 것**:
- pytest 기본 사용법 (fixture, parametrize)
- TestClient로 API 엔드포인트 테스트
- HTTPException과 커스텀 예외 핸들러
- Python logging 모듈과 미들웨어 로깅
- pydantic-settings로 .env 파일 관리
- pytest-cov로 테스트 커버리지 측정

**완료 시나리오**:
```bash
# 테스트 실행
pytest --cov=app --cov-report=html

# 환경 변수 로드
ENVIRONMENT=production uvicorn app.main:app

# 커버리지 90% 이상 달성
```

---

### 🎯 4단계: 데이터베이스 연결 및 관리

**파일**: [`04_DATABASE_GUIDE.md`](./04_DATABASE_GUIDE.md)

**목표**:
- SQLAlchemy ORM 학습
- PostgreSQL 연결 및 설정
- CRUD 작업 구현
- 데이터 마이그레이션 관리

**학습 시간**: 5-7시간
**난이도**: ⭐⭐ (중간)

**이 단계에서 배울 것**:
- 데이터베이스 선택 기준 (3가지 인기 방식 비교)
- PostgreSQL 설치 및 초기 설정
- SQLAlchemy ORM 기초
- 데이터 모델 정의 (User, Post 예제)
- CRUD 함수 작성
- Pydantic 스키마로 검증
- FastAPI 엔드포인트와 데이터베이스 통합
- Alembic으로 마이그레이션 관리
- 테스트 코드 작성

**인기 있는 데이터베이스 연결 방법 3가지**:
1. **SQLAlchemy + PostgreSQL** (가장 권장) ⭐⭐⭐⭐⭐
   - 관계형 데이터베이스, 강력한 ORM, 마이그레이션 지원
   - 프로덕션 프로젝트에 최적
2. **MongoDB + Motor** (NoSQL)
   - 빠른 프로토타입, 유연한 스키마, 비동기 처리
3. **SQLite** (로컬/테스트)
   - 설정 간단, 소규모 프로젝트 최적

**완료 시나리오**:
```bash
# PostgreSQL 시작
brew services start postgresql

# 데이터베이스 및 사용자 생성
psql -U postgres -c "CREATE DATABASE kaira_db;"

# 마이그레이션 실행
alembic upgrade head

# API 테스트
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john", "email": "john@example.com", "password": "pass"}'

# 게시물 생성
curl -X POST "http://localhost:8000/api/posts/?author_id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "첫 게시물", "content": "내용"}'
```

---

### 🎯 5단계: Docker 컨테이너화

**파일**: [`05_DOCKER_GUIDE.md`](./05_DOCKER_GUIDE.md)

**목표**:
- Dockerfile 작성
- Docker 이미지 빌드
- 컨테이너 실행
- docker-compose 활용 (PostgreSQL 포함)

**학습 시간**: 2-3시간
**난이도**: ⭐⭐⭐ (중상)

**이 단계에서 배울 것**:
- Docker 개념 (이미지, 컨테이너, 레지스트리)
- Dockerfile 작성 (Poetry 프로젝트용)
- Multi-stage 빌드로 이미지 최적화
- docker-compose.yml 작성 (FastAPI + PostgreSQL)
- 개발/프로덕션 환경 분리
- Nginx 리버스 프록시 설정

**완료 시나리오**:
```bash
# 개발 환경
docker-compose up -d
# http://localhost:8000 에서 핫 리로딩 확인
# PostgreSQL 자동 실행

# 프로덕션 빌드
docker build -t kaira-server -f Dockerfile.prod .
docker run -p 80:80 kaira-server
# http://localhost 에서 최적화된 이미지 실행
```

---

### 🎯 6단계: 클라우드 배포

**파일**: [`05_CLOUD_DEPLOYMENT_GUIDE.md`](./05_CLOUD_DEPLOYMENT_GUIDE.md)

**목표**:
- 클라우드 인스턴스에 배포
- 도메인 연결
- SSL 인증서 설치
- 모니터링 및 로깅

**학습 시간**: 6-8시간
**난이도**: ⭐⭐⭐⭐ (상)

**이 단계에서 배울 것**:
- AWS EC2 인스턴스 생성 및 설정
- Docker를 EC2에 설치 및 배포
- 도메인 구매 및 DNS 설정
- Let's Encrypt SSL 인증서 발급
- Nginx HTTPS 리버스 프록시
- GitHub Actions CI/CD 자동화
- CloudWatch 로그 및 모니터링
- 무중단 배포 전략 (Blue-Green)

**완료 시나리오**:
```bash
# SSH 접속
ssh -i key.pem ubuntu@<EC2_IP>

# Docker로 배포
docker-compose -f docker-compose.prod.yml up -d

# 실제 도메인에서 HTTPS 서비스
https://yourdomain.com
```

**선택지**:
- **AWS EC2** (가장 유연, 초보자 친화적) ← 메인으로 다룸
- **GCP App Engine** (서버리스, 관리 최소화)
- **Azure App Service** (엔터프라이즈, 기능 많음)

---

## 🗂️ 문서 구조

```
docs/
├── INDEX.md                           # ← 현재 파일
├── 01_FASTAPI_CLI_GUIDE.md           # ✅ 완성 (FastAPI 기초)
├── 02_POETRY_GUIDE.md                # ✅ 완성 (의존성 관리)
├── 03_TESTING_LOGGING_GUIDE.md       # ✅ 완성 (테스트/로깅)
├── 04_DATABASE_GUIDE.md              # ✅ 완성 (데이터베이스)
├── 05_DOCKER_GUIDE.md                # ✅ 완성 (컨테이너화)
└── 06_CLOUD_DEPLOYMENT_GUIDE.md      # ✅ 완성 (클라우드 배포)
```

---

## 🚀 빠른 시작

### 현재 상태

- ✅ **1단계**: FastAPI-CLI 가이드 완성
- ✅ **2단계**: Poetry 가이드 완성
- ✅ **3단계**: 테스트 및 로깅 가이드 완성
- ✅ **4단계**: 데이터베이스 연결 가이드 완성
- ✅ **5단계**: Docker 컨테이너화 가이드 완성
- ✅ **6단계**: 클라우드 배포 가이드 완성

**🎉 전체 로드맵 작성 완료!**

### 지금 할 수 있는 것

1. 1단계부터 순차적으로 시작하기: [`01_FASTAPI_CLI_GUIDE.md`](./01_FASTAPI_CLI_GUIDE.md)
2. 특정 단계만 보고 싶다면:
   - 의존성 관리 배우기 → [`02_POETRY_GUIDE.md`](./02_POETRY_GUIDE.md)
   - 테스트 작성법 → [`03_TESTING_LOGGING_GUIDE.md`](./03_TESTING_LOGGING_GUIDE.md)
   - 데이터베이스 연결 → [`04_DATABASE_GUIDE.md`](./04_DATABASE_GUIDE.md)
   - Docker 사용법 → [`05_DOCKER_GUIDE.md`](./05_DOCKER_GUIDE.md)
   - 실제 배포하기 → [`06_CLOUD_DEPLOYMENT_GUIDE.md`](./06_CLOUD_DEPLOYMENT_GUIDE.md)
3. 로컬에서 직접 실습하기

**예상 총 학습 시간**: 약 25-35시간 (실습 포함)

---

## 💡 학습 팁

### 1. 단계별로 진행하기
- 각 단계를 완료 후 다음 단계로 진행
- 이전 단계로 돌아가 복습하기 (특히 2단계에서)

### 2. 실습하기
- 문서만 읽지 말고 직접 손으로 코드 입력
- 명령어 복사-붙여넣기 피하기
- 에러 메시지를 자세히 읽기

### 3. 문서 활용
- 공식 문서 우선 (ChatGPT보다 정확함)
  - FastAPI: https://fastapi.tiangolo.com
  - Poetry: https://python-poetry.org
  - Docker: https://docs.docker.com
  - AWS: https://docs.aws.amazon.com

### 4. 기록 남기기
- 각 단계별 배운 점 정리
- 어려웠던 부분 메모
- 나만의 체크리스트 작성

---

## 📅 권장 학습 일정

**총 기간**: 2-4주 (개인 공부 기준)

| 주차 | 단계 | 일정 |
|------|------|------|
| 1주 | 1단계 | Mon-Wed: 학습 / Thu-Fri: 심화 |
| 2주 | 2단계 | Mon-Wed: 학습 / Thu-Fri: 통합 테스트 |
| 3주 | 3-4단계 | Mon-Wed: 테스트 / Thu-Fri: Docker |
| 4주 | 5단계 | Mon-Thu: 배포 / Fri: 최종 점검 |

**유연성**: 원하는 속도로 진행 가능 (빠르거나 느릴 수 있음)

---

## ✅ 학습 완료 후

모든 단계를 완료하면 다음을 할 수 있게 됩니다:

**기술 스킬**:
- ✅ FastAPI로 REST API 설계 및 구현
- ✅ 테스트 코드 작성
- ✅ Docker로 앱 배포
- ✅ 클라우드 인스턴스 관리
- ✅ CI/CD 파이프라인 이해

**실전 경험**:
- ✅ 로컬 개발 환경 구축
- ✅ 프로덕션급 코드 작성
- ✅ 실제 인스턴스에 배포
- ✅ 모니터링 및 로깅 운영

**다음 스텝**:
- Django로 풀스택 웹 개발
- 데이터베이스 (PostgreSQL, MongoDB)
- 마이크로서비스 아키텍처
- Kubernetes 배포

---

## 🎓 이 학습의 특징

### ✨ 왜 이 방식인가?

**1단계 (CLI) → 2단계 (Poetry) 순서의 장점:**

| 특징 | 설명 |
|------|------|
| **단계적 진행** | 쉬운 것부터 어려운 것으로 |
| **복습 효과** | 같은 코드를 다른 방식으로 재구성 |
| **비교 학습** | CLI vs Poetry 차이 자연스럽게 이해 |
| **포기 방지** | 초반에 성공 경험으로 동기부여 |
| **실무 적용** | 각 단계가 실제 프로젝트에 직접 사용 가능 |

### 📝 문서의 특징

- **이론 + 실습**: 설명 + 실행 명령어 병행
- **체크리스트**: 각 단계 완료 여부 확인
- **팁과 주의사항**: 자주 하는 실수 사전 방지
- **참고 자료**: 더 깊게 학습할 수 있는 링크

---

## 🆘 도움말

### 문제 해결

**문제**: 명령어가 실행되지 않음
- 터미널에서 에러 메시지 전체 읽기
- 경로 확인 (`pwd`, `ls`)
- 가상환경 활성화 확인 (`which python`)

**문제**: 포트가 이미 사용 중
```bash
# 포트 변경
uvicorn main:app --port 8001 --reload
```

**문제**: 모듈을 찾을 수 없음
```bash
# 의존성 재설치
pip install -r requirements.txt
```

### 자주 묻는 질문 (FAQ)

**Q: 모든 단계를 한 번에 해야 하나요?**
A: 아니요. 각 단계별로 완전히 이해한 후 진행하세요.

**Q: 단계를 건너뛸 수 있나요?**
A: 권장하지 않습니다. 각 단계가 다음 단계의 기초입니다.

**Q: 배포 후 어떻게 해야 하나요?**
A: [클라우드 배포 가이드](./05_CLOUD_DEPLOYMENT_GUIDE.md)의 "모니터링" 섹션 참조.

---

## 📞 피드백

학습 중 문제나 제안이 있으면:

1. 해당 챕터의 "문제 해결" 섹션 확인
2. 공식 문서 검색
3. 로컬 이슈 정리 (무엇을 시도했는지)

---

## 🎉 시작할 준비가 됐나요?

**다음 단계**: [`01_FASTAPI_CLI_GUIDE.md`](./01_FASTAPI_CLI_GUIDE.md)로 이동

행운을 빕니다! 🚀

---

**마지막 업데이트**: 2025년 10월 21일
**현재 완성도**: 1단계 ✅ | 2-5단계 ⏳
