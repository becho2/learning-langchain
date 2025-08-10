from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

completion = model.invoke("Hi there!")
# Hi!

completions = model.batch(["Hi there!", "Bye!"])
# ['Hi!', 'See you!']

for token in model.stream("Bye!"):
    print(token)
    # Good
    # bye
    # !
