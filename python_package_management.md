# Python 패키지 관리 가이드

## 📦 Python 패키지란?

Python에서 **패키지(package)**는 코드를 조직화하고 재사용하기 위한 단위입니다. 여러 모듈을 그룹화하여 계층적으로 관리할 수 있습니다.

### 패키지 vs 모듈

- **모듈(Module)**: 단일 `.py` 파일 (예: `utils.py`).
- **패키지(Package)**: 여러 모듈을 포함하는 디렉터리로, `__init__.py` 파일이 있어야 패키지로 인식됩니다.

## 🗂️ 패키지를 구분짓는 요소

### 1. `__init__.py` 파일

- **역할**: 디렉터리를 "패키지"로 선언.
- **내용**: 보통 비어 있거나 패키지 초기화 코드 포함.

**예시**:

```text
mypackage/
├── __init__.py      # 패키지 선언
├── module1.py
└── module2.py
```

- `import mypackage` → `__init__.py` 실행 후 패키지 로드.

### 2. 디렉터리 구조

- **역할**: 패키지의 계층 형성 (서브패키지).

**예시**:

```text
project/
├── __init__.py
├── utils/
│   ├── __init__.py    # 서브패키지
│   └── helpers.py
└── main.py
```

- `import project.utils.helpers`

### 3. Import 경로와 이름

- **역할**: 패키지를 고유하게 식별 (점`.`으로 구분).
- **예시**: `from mypackage.utils import helper`

## 🔍 Import 시스템과 sys.path

### sys.path란?

- Python이 `import`할 때 모듈을 찾는 디렉터리 리스트.
- **자동 추가 경로**:
  - Python 설치 경로.
  - `PYTHONPATH` 환경 변수.
  - 현재 작업 디렉터리.
  - 스크립트/도구 실행 시 추가 경로.

### Import 메커니즘

- **절대 Import**: `from main import app` → `sys.path` 순서대로 검색.
- **상대 Import**: `from . import submodule` (현재 패키지 내), `from .. import parent` (상위 패키지).
- **장점**: `sys.path`에 경로를 추가하면 상대 경로(`../`) 없이 깔끔한 절대 import 가능.

### sys.path 확인 방법

```python
import sys
print("sys.path:")
for path in sys.path:
    print(f"  {path}")
```

## 🧪 Pytest와 패키지

### Pytest의 경로 설정

- 테스트 실행 시 `conftest.py`가 있는 디렉터리와 상위 디렉터리를 `sys.path`에 추가.
- **예시**: `tests/conftest.py`에서 `from main import app` 가능 (상위 `main.py` import).

### 실행 예시

```text
kaira-server/
├── main.py
└── tests/
    ├── __init__.py
    └── conftest.py  # from main import app
```

- Pytest 실행 시 `sys.path`에 `kaira-server/` 추가 → `main.py` 찾음.

### 확인 코드

```python
# conftest.py에 추가
import sys
print("sys.path in pytest:")
for path in sys.path:
    print(f"  {path}")
```

## 📋 패키지 관리 팁

### 1. 프로젝트 구조 권장

```text
project/
├── __init__.py
├── main.py
├── package/
│   ├── __init__.py
│   └── module.py
└── tests/
    ├── __init__.py
    └── conftest.py
```

### 2. Import 스타일

- **절대 Import 우선**: `from package.module import func`
- **상대 Import**: 패키지 내에서만 사용.

### 3. 환경 설정

- **PYTHONPATH**: `export PYTHONPATH=/path/to/project:$PYTHONPATH`
- **sys.path 수동 추가**: `sys.path.insert(0, '/path/to/project')`

### 4. 주의점

- `__init__.py`는 패키지 선언이지 import 경로 결정이 아님.
- 같은 이름 모듈 충돌 시 `sys.path` 순서에 따라 우선 로드.

## 🎯 핵심 요약

- **패키지 선언**: `__init__.py` + 디렉터리.
- **Import 검색**: `sys.path` 순서대로.
- **Pytest**: 자동 경로 설정으로 테스트 환경 일관성 유지.
- **장점**: 상대 경로 없이 모듈화된 코드 작성 가능.

이 가이드를 통해 Python 패키지를 효과적으로 관리하세요! 📚