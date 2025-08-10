# 🎨 Pretty Print 간단 가이드

## 방법 1: Python 내장 pprint (가장 간단!)
```python
from pprint import pprint

# 그냥 print 대신 pprint 사용
pprint(result)
```

## 방법 2: JSON으로 예쁘게 출력
```python
import json

# Dictionary나 List를 예쁘게
print(json.dumps(result, indent=2, ensure_ascii=False))
```

## 방법 3: 헬퍼 함수 만들어서 사용
```python
# 파일 상단에 한 번만 추가
from pprint import pprint as pp

# 사용할 때
pp(result)  # print(result) 대신
```

## 방법 4: 전체 프로젝트에서 재사용
```python
# pretty_print_helper.py import
from pretty_print_helper import pp

# 사용
pp(result)
```

## 실제 사용 예제

### 기본 print (보기 어려움)
```python
print(result)
# {'messages': [HumanMessage(content='hi', additional_kwargs={}, ....), AIMessage(...)]}
```

### pprint 사용 (자동 줄바꿈)
```python
from pprint import pprint
pprint(result)
# {'messages': [HumanMessage(content='hi',
#                           additional_kwargs={},
#                           response_metadata={}),
#              AIMessage(content='Hello!',
#                       additional_kwargs={})]}
```

### JSON 형식 (가장 깔끔)
```python
import json
# LangChain 객체는 dict()로 변환 필요
if hasattr(result, 'dict'):
    print(json.dumps(result.dict(), indent=2, ensure_ascii=False))
```

## 💡 팁
- `pprint`는 import만 하면 바로 사용 가능 (가장 간단!)
- `json.dumps`는 한글도 예쁘게 출력 (`ensure_ascii=False`)
- 실습할 때는 그냥 `from pprint import pprint as pp` 한 줄만 추가하고 `pp()` 사용!