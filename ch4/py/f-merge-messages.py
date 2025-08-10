from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
    merge_message_runs,
)
# Pretty print - Python 내장 모듈만 사용!
from pprint import pprint as pp
import json


# Sample messages with consecutive messages of same type
messages = [
    SystemMessage(content="you're a good assistant."),
    SystemMessage(content="you always respond with a joke."),
    HumanMessage(
        content=[{"type": "text", "text": "i wonder why it's called langchain"}]
    ),
    HumanMessage(content="and who is harrison chasing anyways"),
    AIMessage(
        content='Well, I guess they thought "WordRope" and "SentenceString" just didn\'t have the same ring to it!'
    ),
    AIMessage(
        content="Why, he's probably chasing after the last cup of coffee in the office!"
    ),
]

# Merge consecutive messages
merged = merge_message_runs(messages)

print("\n=== 기본 print (보기 어려움) ===")
print(merged)

print("\n=== pprint 사용 (자동 줄바꿈) ===")
pp(merged)

print("\n=== JSON 형식 (가장 깔끔) ===")
# LangChain 메시지를 dict로 변환 (Pydantic v2 호환)
merged_dict = []
for msg in merged:
    if hasattr(msg, 'model_dump'):
        merged_dict.append(msg.model_dump())  # Pydantic v2
    elif hasattr(msg, 'dict'):
        merged_dict.append(msg.dict())  # Pydantic v1
    else:
        merged_dict.append(msg)
print(json.dumps(merged_dict, indent=2, ensure_ascii=False))
