from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
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


# Add the chatbot node
builder.add_node("chatbot", chatbot)

# Add edges
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile()

# Run the graph
input = {"messages": [HumanMessage("hi!")]}
for chunk in graph.stream(input):
    print(chunk)
