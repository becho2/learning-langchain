from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import chain

# the building blocks

template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        ("human", "{question}"),
    ]
)

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# combine them in a function
# @chain decorator adds the same Runnable interface for any function you write


@chain
def chatbot(values):
    prompt = template.invoke(values)
    return model.invoke(prompt)


# use it

response = chatbot.invoke({"question": "Which model providers offer LLMs?"})
print(response.content)
