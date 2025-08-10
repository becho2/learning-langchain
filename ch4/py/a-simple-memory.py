from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer all questions to the best of         your ability."),
    ("placeholder", "{messages}"),
])

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

chain = prompt | model

response = chain.invoke({
    "messages": [
        ("human", "Translate this sentence from English to French: I love programming."),
        ("ai", "J'adore programmer."),
        ("human", "What did you just say?"),
    ],
})

print(response.content)
