from langchain_core.runnables import chain
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_core.prompts import ChatPromptTemplate


model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")


template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{question}"),
    ]
)


@chain
def chatbot(values):
    prompt = template.invoke(values)
    for token in model.stream(prompt):
        yield token


for part in chatbot.stream({"question": "Which model providers offer LLMs?"}):
    print(part)
