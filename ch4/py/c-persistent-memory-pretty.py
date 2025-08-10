from typing import Annotated, TypedDict
import warnings
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich import box
from rich.syntax import Syntax
import json

# Suppress urllib3 OpenSSL warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', message='urllib3 v2 only supports OpenSSL')

# Disable LangSmith tracing to avoid authentication errors
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
os.environ['LANGSMITH_API_KEY'] = 'dummy'  # Prevents missing key warning

from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.checkpoint.memory import MemorySaver


class State(TypedDict):
    messages: Annotated[list, add_messages]


# Initialize Rich console for pretty printing
console = Console()

# Load environment variables
load_dotenv()

# Build the graph
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


def print_message(message, role="user", conversation_num=None):
    """Pretty print a single message"""
    if role == "user":
        icon = "👤"
        color = "cyan"
        role_text = "Human"
    else:
        icon = "🤖"
        color = "green"
        role_text = "AI"
    
    if conversation_num:
        title = f"{icon} {role_text} - 대화 #{conversation_num}"
    else:
        title = f"{icon} {role_text}"
    
    panel = Panel(
        message,
        title=title,
        title_align="left",
        border_style=color,
        box=box.ROUNDED,
        padding=(0, 1)
    )
    console.print(panel)


def print_conversation_history(messages):
    """Pretty print the entire conversation history"""
    console.print("\n" + "="*60)
    console.print(Text("💬 전체 대화 내역", style="bold magenta", justify="center"))
    console.print("="*60 + "\n")
    
    for i, msg in enumerate(messages, 1):
        if isinstance(msg, HumanMessage):
            print_message(msg.content, "user")
        elif isinstance(msg, AIMessage):
            print_message(msg.content, "ai")
        
        if i < len(messages):
            console.print(Text("↓", style="dim", justify="center"))


def print_state_info(state_snapshot):
    """Pretty print the state information"""
    console.print("\n" + "="*60)
    console.print(Text("📊 상태 정보", style="bold yellow", justify="center"))
    console.print("="*60 + "\n")
    
    # Create a table for state information
    table = Table(show_header=True, header_style="bold cyan", box=box.ROUNDED)
    table.add_column("항목", style="cyan", width=20)
    table.add_column("값", style="white")
    
    # Add state information
    table.add_row("Thread ID", state_snapshot.config['configurable']['thread_id'])
    table.add_row("Checkpoint ID", state_snapshot.config['configurable']['checkpoint_id'][:20] + "...")
    
    # Handle created_at - it might be a string
    if hasattr(state_snapshot, 'created_at'):
        if isinstance(state_snapshot.created_at, str):
            table.add_row("생성 시간", state_snapshot.created_at[:19])
        else:
            table.add_row("생성 시간", state_snapshot.created_at.strftime("%Y-%m-%d %H:%M:%S"))
    
    table.add_row("총 메시지 수", str(len(state_snapshot.values['messages'])))
    
    # Token usage if available
    total_tokens = 0
    for msg in state_snapshot.values['messages']:
        if isinstance(msg, AIMessage) and hasattr(msg, 'usage_metadata'):
            if msg.usage_metadata:
                total_tokens += msg.usage_metadata.get('total_tokens', 0)
    
    if total_tokens > 0:
        table.add_row("총 토큰 사용량", str(total_tokens))
    
    console.print(table)


def print_header():
    """Print a beautiful header"""
    header_text = """
╔══════════════════════════════════════════════════════════╗
║         🎯 LangGraph 메모리 지속성 데모 🎯               ║
║        Persistent Conversation with Memory               ║
╚══════════════════════════════════════════════════════════╝
    """
    console.print(Text(header_text, style="bold blue", justify="center"))


# Main execution
if __name__ == "__main__":
    print_header()
    
    # First conversation
    console.print("\n" + "─"*60)
    console.print(Text("🚀 첫 번째 대화 시작", style="bold green"))
    console.print("─"*60 + "\n")
    
    user_message_1 = "안녕? 내 이름은 참참이야!"
    print_message(user_message_1, "user", 1)
    
    result_1 = graph.invoke({"messages": [HumanMessage(user_message_1)]}, thread1)
    ai_response_1 = result_1['messages'][-1].content
    print_message(ai_response_1, "ai", 1)
    
    # Second conversation
    console.print("\n" + "─"*60)
    console.print(Text("🚀 두 번째 대화 (메모리 테스트)", style="bold green"))
    console.print("─"*60 + "\n")
    
    user_message_2 = "내 이름이 뭐게?"
    print_message(user_message_2, "user", 2)
    
    result_2 = graph.invoke({"messages": [HumanMessage(user_message_2)]}, thread1)
    ai_response_2 = result_2['messages'][-1].content
    print_message(ai_response_2, "ai", 2)
    
    # Show full conversation history
    state = graph.get_state(thread1)
    print_conversation_history(state.values['messages'])
    
    # Show state information
    print_state_info(state)
    
    # Success message
    console.print("\n")
    success_panel = Panel(
        Text("✨ 메모리 지속성 테스트 완료! AI가 이전 대화를 기억하고 있습니다.", style="bold green"),
        title="✅ 성공",
        border_style="green",
        box=box.DOUBLE
    )
    console.print(success_panel)