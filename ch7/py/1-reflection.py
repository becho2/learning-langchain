from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(
  model='gemini-2.5-flash',
  temperature=0.1,
  google_api_key=os.getenv('GOOGLE_API_KEY')
)

# 상태 타입 정의
class State(TypedDict):
  messages: Annotated[list, add_messages]
  
  
# 프롬프트 정의
generate_prompt = SystemMessage(
  '당신은 훌륭한 3단락 에세이를 작성하는 임무를 가진 에세이 어시스턴트입니다.'
  '사용자의 요청에 맞춰 최상의 에세이를 작성하세요.'
  '사용자가 비평을 ㅔㅈ공하면, 이전 시도에 대한 수정 버전을 응답하세요.'
)

reflection_prompt = SystemMessage(
  '당신은 에세이 제출물을 평가하는 교사입니다. 사용자의 제출물에 대해 비평과 추천을 생성하세요.'
  '길이, 깊이, 스타일 등과 같은 구체적인 요구사항을 포함한 자세한 추천을 제공하세요.'
)

def generate(state: State) -> State:
  answer = model.invoke([generate_prompt] + state['messages'])
  return {'messages': [answer]}

def reflect(state: State) -> State:
  cls_map = {AIMessage: HumanMessage, HumanMessage: AIMessage}
  
  translated = [reflection_prompt, state['messages'][0]] + [
    cls_map[msg.__class__](msg.content) for msg in state['messages'][1:]
  ]
  answer = model.invoke(translated)
  return {'messages': [answer]}

def should_continue(state: State):
  if len(state['messages']) > 6:
    return END
  else:
    return 'reflect'

builder = StateGraph(State)
builder.add_node('generate', generate)
builder.add_node('reflect', reflect)

builder.add_edge(START, 'generate')
builder.add_conditional_edges('generate', should_continue)
builder.add_edge('reflect', 'generate')


graph = builder.compile()

# Example usage
initial_state = {
    "messages": [
        HumanMessage(
            content="어린왕자가 현대인들에게 주는 의미에 대해 3단락 에세이를 작성하세요."
        )
    ]
}

# Run the graph
for output in graph.stream(initial_state):
    message_type = "generate" if "generate" in output else "reflect"
    print("\nNew message:", output[message_type]
          ["messages"][-1].content)