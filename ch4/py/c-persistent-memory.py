from typing import Annotated, TypedDict
import warnings
import os

# Suppress urllib3 OpenSSL warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

# Disable LangSmith tracing to avoid authentication errors
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGSMITH_API_KEY'] = 'dummy'  # Prevents missing key warning

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Load environment variables
load_dotenv()

builder = StateGraph(State)

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)


def chatbot(state: State):
    answer = model.invoke(state["messages"])
    return {"messages": [answer]}


builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# Add persistence with MemorySaver
graph = builder.compile(checkpointer=MemorySaver())

# Configure thread
thread1 = {"configurable": {"thread_id": "1"}}

# Run with persistence
result_1 = graph.invoke({"messages": [HumanMessage("안녕? 내 이름은 참참이야!")]}, thread1)
print(result_1)

result_2 = graph.invoke({"messages": [HumanMessage("내 이름이 뭐게?")]}, thread1)
print(result_2)

# Get state
print(graph.get_state(thread1))
