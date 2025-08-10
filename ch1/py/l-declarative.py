from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_core.prompts import ChatPromptTemplate

# the building blocks

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{question}"),
    ]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# combine them with the | operator

chatbot = template | model

# use it

response = chatbot.invoke({"question": "Which model providers offer LLMs?"})
print(response.content)

# streaming

for part in chatbot.stream({"question": "Which model providers offer LLMs?"}):
    print(part)
