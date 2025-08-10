"""
간단한 Pretty Print 헬퍼 - 모든 실습 파일에서 import해서 사용
"""
import json
from pprint import pprint


def pp(obj):
    """
    Pretty print any object - 가장 간단한 방법
    Usage: pp(result)
    """
    pprint(obj, width=80, compact=False)


def ppj(obj):
    """
    Pretty print as JSON - dictionary나 list를 예쁘게
    Usage: ppj(result)
    """
    # Convert LangChain messages to dict if needed
    if hasattr(obj, 'dict'):
        obj = obj.dict()
    elif isinstance(obj, list) and all(hasattr(item, 'dict') for item in obj):
        obj = [item.dict() for item in obj]
    elif isinstance(obj, dict) and 'messages' in obj:
        # Handle graph results
        if isinstance(obj['messages'], list):
            obj = {
                'messages': [
                    msg.dict() if hasattr(msg, 'dict') else msg 
                    for msg in obj['messages']
                ]
            }
    
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def ppm(messages):
    """
    Pretty print messages - 메시지 리스트 전용
    Usage: ppm(messages)
    """
    for i, msg in enumerate(messages, 1):
        print(f"\n--- Message {i} ---")
        if hasattr(msg, '__class__'):
            print(f"Type: {msg.__class__.__name__}")
        if hasattr(msg, 'content'):
            print(f"Content: {msg.content}")
        if hasattr(msg, 'additional_kwargs') and msg.additional_kwargs:
            print(f"Additional: {msg.additional_kwargs}")
        print("-" * 20)