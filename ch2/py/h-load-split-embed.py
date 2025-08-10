import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

# Load the document
loader = TextLoader("./test.txt", encoding="utf-8")
doc = loader.load()

# Split the document
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(doc)

# Generate embeddings
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))
embeddings = embeddings_model.embed_documents(
    [chunk.page_content for chunk in chunks]
)

print(embeddings)
