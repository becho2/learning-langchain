# Warning Suppression Guide

## 문제 설명
실습 중 다음과 같은 불필요한 경고/에러 메시지가 발생합니다:

1. **OpenSSL Warning**: urllib3와 LibreSSL 호환성 문제
2. **LangSmith API Key Warning**: LangSmith API 키 누락 경고
3. **LangSmith Authentication Errors**: LangSmith 트레이싱 인증 실패

## 해결 방법

### 방법 1: 개별 스크립트에 적용
각 Python 스크립트 상단에 다음 코드를 추가하세요:

```python
import warnings
import os

# Suppress urllib3 OpenSSL warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

# Disable LangSmith tracing to avoid authentication errors
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGSMITH_API_KEY'] = 'dummy'  # Prevents missing key warning

# 이후 다른 import 문들...
from langchain_core.messages import HumanMessage
# ...
```

### 방법 2: 전역 설정 파일 사용
`suppress_warnings.py` 파일을 import하여 사용:

```python
import suppress_warnings  # 맨 처음에 import

# 이후 다른 import 문들...
from langchain_core.messages import HumanMessage
# ...
```

### 방법 3: 환경 변수 설정
터미널에서 스크립트 실행 전 환경 변수 설정:

```bash
export LANGCHAIN_TRACING_V2=false
export LANGSMITH_API_KEY=dummy
python3 your_script.py
```

## 원인 설명

### 1. OpenSSL Warning
- **원인**: macOS의 LibreSSL 2.8.3과 urllib3 v2의 호환성 문제
- **영향**: 기능에는 영향 없음, 단순 경고 메시지
- **해결**: warnings.filterwarnings로 경고 숨김

### 2. LangSmith 관련 에러
- **원인**: LangSmith는 LangChain의 관찰성(observability) 도구로, API 키가 필요
- **영향**: 학습/실습에는 불필요, 프로덕션 모니터링용
- **해결**: LANGCHAIN_TRACING_V2를 'false'로 설정하여 비활성화

## 주의사항
- 이 설정은 개발/학습 환경에만 적용하세요
- 프로덕션 환경에서는 적절한 모니터링이 필요할 수 있습니다
- OpenSSL 경고는 무시해도 안전하지만, 가능하면 Python 환경을 업데이트하는 것이 좋습니다