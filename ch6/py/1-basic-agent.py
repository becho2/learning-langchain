from langchain_core.tools import tool
import ast
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from typing import Annotated, TypedDict
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, ToolCall, AIMessage
from pprint import pprint
from uuid import uuid4

load_dotenv()


@tool
def calculater(query: str) -> str:
  '''계산기. 수식만 입력받습니다.'''
  # eval()을 안전하게 사용하기 위해 제한된 환경에서 실행
  # 숫자와 기본 연산자만 허용
  allowed_names = {
      'abs': abs,
      'round': round,
      'min': min,
      'max': max,
  }
  
  # 안전한 수식 평가를 위해 compile과 eval 사용
  try:
      node = ast.parse(query, mode='eval')
      
      # AST를 검사하여 안전한 노드만 허용
      for node in ast.walk(node):
          if isinstance(node, ast.Name) and node.id not in allowed_names:
              raise ValueError(f"사용할 수 없는 이름: {node.id}")
          elif isinstance(node, ast.Call):
              if not isinstance(node.func, ast.Name) or node.func.id not in allowed_names:
                  raise ValueError("허용되지 않은 함수 호출")
      
      # 안전한 경우에만 eval 실행
      code = compile(query, '<string>', 'eval')
      result = eval(code, {"__builtins__": {}}, allowed_names)
      return str(result)
  except Exception as e:
      return f"계산 오류: {str(e)}"

search = DuckDuckGoSearchRun()
tools = [search, calculater]
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=os.getenv("GOOGLE_API_KEY")
).bind_tools(tools)

class State(TypedDict):
  messages: Annotated[list, add_messages]
  
def model_node(state: State) -> State:
  res = model.invoke(state["messages"])
  return {'messages': res}

def first_model(state: State) -> State:
  query = state['messages'][-1].content
  search_tool_call = ToolCall(
    name='duckduckgo_search',
    args={
      'query': query
    },
    id=uuid4().hex 
  )
  print(query)
  return {'messages': AIMessage(content='', tool_calls=[search_tool_call])}

builder = StateGraph(State)
builder.add_node('first_model', first_model)
builder.add_node('model', model_node)
builder.add_node('tools', ToolNode(tools))
builder.add_edge(START, 'first_model')
builder.add_edge('first_model', 'tools')
builder.add_conditional_edges('model', tools_condition)
builder.add_edge('tools', 'model')

graph = builder.compile()

# graph.get_graph().draw_mermaid_png(output_file_path="gsraph.png")

input = {
  'messages': [HumanMessage("이승만 대통령이 대통령이 됐을 때 이승만과 김구의 나이는?")]
}

for c in graph.stream(input):
  pprint(c)
