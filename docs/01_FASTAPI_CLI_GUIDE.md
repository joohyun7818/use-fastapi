# 1단계: FastAPI로 빠른 프로토타입 만들기

> **목표**: 정적 웹사이트를 FastAPI로 서빙하는 프로토타입을 2-3일 만에 완성하기
>
> **학습 시간**: 2-3일
> **난이도**: ⭐ (쉬움)
> **사전 요구사항**: Python 3.10+, 기본 터미널 명령어

---

## 📋 1단계 학습 목표

1단계를 완료하면 다음을 할 수 있게 됩니다:
- ✅ FastAPI 프로젝트를 수동으로 생성
- ✅ 기본 라우팅(`@app.get()`) 이해 및 작성
- ✅ 정적 파일(`kaira-1.0.0`) FastAPI로 마운트
- ✅ Uvicorn으로 로컬 개발 서버 실행
- ✅ Swagger UI/ReDoc 자동 생성된 API 문서 확인
- ✅ 간단한 JSON 응답 반환 및 테스트

**완료 시 결과물**: http://127.0.0.1:8000 에서 정적 웹사이트 서빙 + API 문서 제공

---

## 📚 1단계 목차

| 챕터 | 주제 | 예상 시간 |
|------|------|---------|
| [1.1](#11-사전-준비-확인) | 사전 준비 확인 | 10분 |
| [1.2](#12-fastapi-설치) | FastAPI 설치 | 5분 |
| [1.3](#13-프로젝트-폴더-생성) | 프로젝트 폴더 생성 | 5분 |
| [1.4](#14-mainpy-파일-작성) | main.py 파일 작성 | 15분 |
| [1.5](#15-첫-실행-fastapi-dev-server-시작) | 첫 실행 (FastAPI Dev Server) | 10분 |
| [1.6](#16-api-문서-확인-swagger) | API 문서 확인 (Swagger) | 10분 |
| [1.7](#17-기본-엔드포인트-이해) | 기본 엔드포인트 이해 | 20분 |
| [1.8](#18-정적-파일-마운트) | 정적 파일 마운트 | 20분 |
| [1.9](#19-새-엔드포인트-추가) | 새 엔드포인트 추가 | 20분 |
| [1.10](#110-테스트-작성) | 테스트 작성 | 20분 |
| [1.11](#111-학습-체크리스트) | 학습 체크리스트 | - |

---

## 1.1 사전 준비 확인

### 현재 환경 확인

이 튜토리얼을 시작하기 전에 다음이 설치되어 있는지 확인하세요.

**Python 버전 확인**:
```bash
python3 --version
# 또는
python --version
```

**예상 결과**: `Python 3.10.x` 이상

❌ 만약 `Python 3.10` 미만이라면 [python.org](https://www.python.org)에서 최신 버전 설치

**Pip 확인**:
```bash
pip --version
```

**예상 결과**: `pip 20.0.0` 이상

**현재 가상환경 상태 확인**:
```bash
which python3
```

**예상 결과 (예시)**:
```
/usr/bin/python3        # 시스템 Python (아직 가상환경 없음)
```

또는 이미 가상환경에 있다면:
```
/Users/joohyun/joohyun/python/fast-api/fastEnv/bin/python
```

### 기존 가상환경 활성화

현재 `fastEnv/`라는 가상환경이 이미 있으므로, 이를 사용합니다.

**macOS/Linux에서 활성화**:
```bash
source fastEnv/bin/activate
```

**활성화 확인**:
```bash
which python
```

**예상 결과**:
```
/Users/joohyun/joohyun/python/fast-api/fastEnv/bin/python
```

터미널 프롬프트 앞에 `(fastEnv)`가 표시되어야 합니다:
```
(fastEnv) user@machine:~/python/fast-api $
```

### 작업 디렉터리 정리

현재 디렉터리 구조:
```
/Users/joohyun/joohyun/python/fast-api/
├── fastEnv/              # 가상환경 ✓
├── kaira-1.0.0/          # 정적 웹사이트 ✓
├── test_app/
└── LEARNING_ROADMAP.md   # 로드맵 문서
```

**이 단계에서 새로 만들 것**:
```
├── kaira-server/         # ← 새 FastAPI 프로젝트 (fastapi new로 생성)
```

---

## 1.2 FastAPI 설치

### FastAPI와 Uvicorn 설치

가상환경이 활성화된 상태에서 다음을 실행합니다:

```bash
pip install fastapi uvicorn[standard]
```

**설치 항목 설명**:
- `fastapi`: FastAPI 프레임워크
- `uvicorn[standard]`: ASGI 서버 (WebSocket, HTTP/2 지원)

### 설치 확인

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

**예상 결과**:
```
0.115.0 (또는 최신 버전)
```

```bash
uvicorn --version
```

**예상 결과**:
```
Running uvicorn 0.30.x
```

✅ **완료**: FastAPI가 준비됐습니다!

---

## 1.3 프로젝트 폴더 생성

### 프로젝트 디렉터리 만들기

```bash
mkdir kaira-server
cd kaira-server
```

### 필요한 파일 구조 준비

```bash
# main.py 파일을 만들 준비 (다음 섹션에서 작성)
# 지금은 폴더만 생성
pwd
```

**예상 결과**:
```
/Users/joohyun/joohyun/python/fast-api/kaira-server
```

✅ **완료**: 프로젝트 폴더가 준비되었습니다!

---

## 1.4 main.py 파일 작성

### 기본 FastAPI 앱 작성

`main.py` 파일을 생성하고 다음 내용을 입력합니다:

**VS Code에서 열기**:
```bash
code main.py
```

**또는 nano/vim 사용**:
```bash
nano main.py
```

**main.py 내용**:
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

**파일 저장**:
- VS Code: `Cmd + S`
- nano: `Ctrl + O`, Enter, `Ctrl + X`

### 파일 확인

```bash
cat main.py
```

**예상 출력**:
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

✅ **완료**: 첫 FastAPI 앱이 준비되었습니다!

---

## 1.5 첫 실행: FastAPI Dev Server 시작

### fastapi dev 명령으로 실행 (권장)

프로젝트 폴더(`kaira-server/`)에서 다음 명령을 실행합니다:

```bash
fastapi dev main.py
```

**명령어 설명**:
- `fastapi dev`: FastAPI 개발 서버 (Uvicorn 래퍼, 권장 방식)
- `main.py`: 앱이 들어 있는 파일명
- 자동으로 `--reload` 적용 (코드 변경 시 자동 재시작)

**터미널에 보이는 메시지**:
```
 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/Users/joohyun/joohyun/python/fast-api/kaira-server']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using WatchFiles
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 대안: uvicorn 직접 사용

만약 `fastapi` 명령이 없다면 Uvicorn을 직접 사용할 수 있습니다:

```bash
uvicorn main:app --reload
```

### 서버가 실행 중인지 확인

**현재 상태**:
- ✅ 서버가 `http://127.0.0.1:8000`에서 실행 중
- ✅ 자동 리로드 활성화 (코드 변경하면 자동 재시작)
- ✅ 개발 모드 (DEBUG 로그 보임)

### 다른 터미널에서 요청 보내기

**새 터미널 창**을 열어서 (서버는 계속 실행 상태로 두기):

```bash
curl http://127.0.0.1:8000
```

**예상 응답**:
```json
{"Hello":"World"}
```

✅ **성공**: FastAPI 서버가 정상 작동하고 있습니다!

---

## 1.6 API 문서 확인 (Swagger)

### Swagger UI 접근

브라우저에서 다음 주소를 방문합니다:

```
http://127.0.0.1:8000/docs
```

### 화면에 보이는 것

```
FastAPI                          ← 앱 제목

/                                ← 엔드포인트
├─ GET
│  └─ Parameters: 없음
│     Response: {"Hello": "World"}
```

**Try it out 버튼**을 클릭하면:
1. "Execute" 버튼이 나타남
2. 클릭하면 실제 요청 발송
3. 응답이 JSON으로 표시됨

### ReDoc 문서 확인 (선택)

```
http://127.0.0.1:8000/redoc
```

Swagger와 유사하지만 더 깔끔한 문서 형식입니다.

**핵심 포인트**:
> FastAPI는 자동으로 OpenAPI 스키마를 생성하고, Swagger UI와 ReDoc 문서를 제공합니다!
> 다른 웹 프레임워크에서는 이런 문서를 직접 작성해야 합니다.

---

## 1.7 기본 엔드포인트 이해

### 현재 엔드포인트 분석

`main.py`를 다시 보면:

```python
@app.get("/")
def read_root():
    return {"Hello": "World"}
```

**각 부분 설명**:

| 부분 | 설명 | 예시 |
|------|------|------|
| `@app.get("/")` | 데코레이터: "GET 요청이 `/`로 들어오면 이 함수 실행" | `@app.post()`, `@app.put()` 등도 가능 |
| `/` | 경로(Path): 엔드포인트 경로 | `/items`, `/api/users` 등 |
| `read_root()` | 함수명: 자유롭게 지정 가능 | 의미 있게 작성할 것 |
| `return {...}` | 반환값: Python 딕셔너리는 JSON으로 자동 변환 | `{"key": "value"}` |

### HTTP 메서드 (Methods)

**GET**: 데이터를 받아오기
```python
@app.get("/")
def get_data():
    return {"data": "some value"}
```

**POST**: 데이터를 보내기
```python
@app.post("/items")
def create_item(item_name: str):
    return {"created": item_name}
```

**PUT**: 데이터를 수정하기
```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item_name: str):
    return {"item_id": item_id, "new_name": item_name}
```

**DELETE**: 데이터를 삭제하기
```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"deleted": item_id}
```

### 경로 매개변수 (Path Parameters)

엔드포인트 경로에 변수를 포함할 수 있습니다:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

**요청 예시**:
- `GET /items/42` → `{"item_id": 42}`
- `GET /items/100` → `{"item_id": 100}`

**타입 힌트**:
- `item_id: int` - item_id는 정수여야 함
- `item_id: str` - item_id는 문자열
- `item_id: float` - item_id는 실수

타입이 맞지 않으면 FastAPI가 자동으로 400 에러 반환합니다!

---

## 1.8 정적 파일 마운트

### 목표

현재 `kaira-1.0.0/` 폴더의 웹사이트를 FastAPI에서 서빙하기

### StaticFiles 임포트

`main.py` 파일을 수정합니다:

**현재 내용**:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

**수정 후**:
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

# 정적 파일 마운트
static_dir = Path(__file__).parent.parent / "kaira-1.0.0"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
```

### 코드 설명

**`from fastapi.staticfiles import StaticFiles`**:
- 정적 파일 (HTML, CSS, JS, 이미지) 을 서빙하는 기능

**`Path(__file__).parent.parent / "kaira-1.0.0"`**:
- `__file__`: 현재 파일 경로 (main.py)
- `.parent`: 상위 폴더 (kaira-server/)
- `.parent`: 그 위 폴더 (fast-api/)
- `/`: 다음 폴더
- 결과: `/Users/joohyun/joohyun/python/fast-api/kaira-1.0.0`

**`app.mount("/static", ...)`**:
- `/static` 경로로 들어오는 모든 요청을 StaticFiles에 전달
- 예: `/static/index.html`, `/static/css/style.css` 등

**`html=True`**:
- 디렉터리 요청 시 `index.html`을 자동으로 반환
- `/static/` → `/static/index.html` 자동 처리

### 테스트

서버가 여전히 실행 중이면, 코드 변경을 감지해 자동 재시작됩니다.

**확인 (새 터미널에서)**:
```bash
curl http://127.0.0.1:8000/static/
```

**예상 응답**:
HTML 내용 (kaira-1.0.0/index.html)

또는 브라우저에서:
```
http://127.0.0.1:8000/static/
```

`kaira-1.0.0/index.html`이 렌더링되어야 합니다.

---

## 1.9 새 엔드포인트 추가

### API 엔드포인트 추가

현재 `main.py`에 새 엔드포인트를 추가합니다:

**현재 내용**:
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

static_dir = Path(__file__).parent.parent / "kaira-1.0.0"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
```

**새 엔드포인트 추가**:
```python
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI(
    title="Kaira Server",
    version="0.1.0",
    description="Kaira 웹사이트를 서빙하는 FastAPI 서버"
)

@app.get("/")
def read_root():
    """루트 경로"""
    return {"message": "Welcome to Kaira Server!", "status": "ok"}

@app.get("/health")
def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "kaira-server"}

@app.get("/api/info")
def get_info():
    """서버 정보"""
    return {
        "name": "Kaira Server",
        "version": "0.1.0",
        "description": "정적 웹사이트 서빙 서버"
    }

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    """ID로 아이템 조회"""
    return {
        "item_id": item_id,
        "name": f"Item {item_id}",
        "description": f"This is item number {item_id}"
    }

# 정적 파일 마운트
static_dir = Path(__file__).parent.parent / "kaira-1.0.0"
app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")
```

### 추가된 엔드포인트 설명

| 엔드포인트 | 메서드 | 설명 |
|-----------|--------|------|
| `/` | GET | 루트 경로, 서버 상태 확인 |
| `/health` | GET | 헬스 체크 (배포 시 모니터링용) |
| `/api/info` | GET | 서버 정보 조회 |
| `/api/items/{item_id}` | GET | ID로 아이템 조회 |

### 테스트

**Swagger UI에서 확인**:
```
http://127.0.0.1:8000/docs
```

모든 엔드포인트가 리스트에 표시됩니다!

**각 엔드포인트 테스트**:

```bash
# 루트
curl http://127.0.0.1:8000/

# 헬스 체크
curl http://127.0.0.1:8000/health

# 서버 정보
curl http://127.0.0.1:8000/api/info

# 아이템 조회
curl http://127.0.0.1:8000/api/items/42
```

---

## 1.10 테스트 작성

### 테스트 폴더 생성

```bash
mkdir tests
cd tests
touch __init__.py
touch test_main.py
cd ..
```

### 테스트 파일 작성

`tests/test_main.py` 파일을 생성하고 다음 내용을 입력합니다:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Kaira Server!", "status": "ok"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_get_item():
    response = client.get("/api/items/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42
```

### pytest 설치 및 실행

```bash
# pytest 설치
pip install pytest

# 테스트 실행
pytest tests/
```

**예상 결과**:
```
============================= test session starts ==============================
collected 3 items

tests/test_main.py ...                                                  [100%]

============================== 3 passed in 0.50s ===============================
```

### requirements.txt 업데이트

프로젝트의 의존성을 기록합니다:

```bash
pip freeze > requirements.txt
```

**requirements.txt 확인**:
```bash
cat requirements.txt
```

**예상 내용**:
```
fastapi==0.115.0
uvicorn==0.30.0
pytest==7.4.0
...
```

✅ **완료**: 테스트가 정상 작동하고 있습니다!

---

## 1.11 학습 체크리스트

이 섹션을 완료했는지 확인하세요!

### 필수 체크리스트

- [ ] **설치 완료**
  - [ ] Python 3.10+ 설치됨
  - [ ] `fastapi`, `uvicorn` 설치됨
  - [ ] `python -c "import fastapi"` 명령어 작동함

- [ ] **프로젝트 생성**
  - [ ] `kaira-server` 폴더 생성됨
  - [ ] `main.py` 파일 작성됨
  - [ ] 기본 FastAPI 앱 코드 작성됨

- [ ] **로컬 실행**
  - [ ] `uvicorn main:app --reload` 명령으로 서버 실행됨
  - [ ] `http://127.0.0.1:8000/` 에서 응답 받음
  - [ ] `curl` 또는 브라우저에서 JSON 응답 확인됨

- [ ] **API 문서 확인**
  - [ ] Swagger UI (`/docs`) 접근 가능
  - [ ] ReDoc (`/redoc`) 접근 가능
  - [ ] 모든 엔드포인트 문서화됨

- [ ] **엔드포인트 작성**
  - [ ] 최소 4개의 엔드포인트 작성 (`/`, `/health`, `/api/info`, `/api/items/{id}`)
  - [ ] 각 엔드포인트가 정상 응답함

- [ ] **정적 파일 서빙**
  - [ ] StaticFiles 마운트 완료
  - [ ] `/static/` 경로로 접근 가능
  - [ ] `kaira-1.0.0/index.html` 렌더링됨

- [ ] **테스트**
  - [ ] `tests/` 폴더 생성
  - [ ] `test_main.py` 작성
  - [ ] `pytest tests/` 실행 성공
  - [ ] 모든 테스트 통과

### 심화 체크리스트 (선택)

- [ ] 새 엔드포인트 3개 이상 추가 작성
- [ ] 엔드포인트에 쿼리 매개변수 추가 (예: `?name=value`)
- [ ] 에러 핸들링 추가 (예: item_id가 음수면 에러)
- [ ] 자동 문서에서 docstring 활용해 엔드포인트 설명 추가

### 마지막 확인

**아래 명령을 모두 성공적으로 실행했나요?**

```bash
# 1. 프로젝트 폴더로 이동
cd kaira-server

# 2. 서버 실행
uvicorn main:app --reload

# 3. 새 터미널에서
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/info
curl http://127.0.0.1:8000/static/

# 4. 테스트
pytest tests/
```

✅ **모두 성공하면 1단계 완료입니다!**

---

## 📖 다음 단계

1단계를 완료했으면 준비가 됐습니다!

**다음 선택지:**

- **→ 2단계로 진행**: `02_POETRY_GUIDE.md` 읽기
  - 같은 프로젝트를 Poetry로 재구성
  - 의존성 관리 학습
  - 프로덕션 구조 이해

- **→ 1단계 심화**: 더 많은 엔드포인트 추가
  - 쿼리 매개변수 학습
  - 요청 바디 (POST) 학습
  - 더 복잡한 응답 구조

---

## 🎯 1단계 정리

| 항목 | 학습 내용 |
|------|---------|
| **설치** | FastAPI, Uvicorn |
| **명령어** | `uvicorn main:app --reload` |
| **개념** | 엔드포인트, 경로 매개변수, HTTP 메서드 |
| **파일** | main.py, requirements.txt, tests/ |
| **실행** | 로컬 개발 서버 |
| **문서** | Swagger UI (/docs), ReDoc (/redoc) |
| **배운 점** | FastAPI는 자동으로 타입 검증, 문서 생성, JSON 변환을 함! |

---

## ✨ 축하합니다!

1단계 완료! 이제 FastAPI의 기초를 마스터했습니다. 🚀
