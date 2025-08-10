from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
system_msg = SystemMessage(
    "You are a helpful assistant that responds to questions with three exclamation marks."
)
human_msg = HumanMessage("What is the capital of France?")

response = model.invoke([system_msg, human_msg])
print(response.content)
