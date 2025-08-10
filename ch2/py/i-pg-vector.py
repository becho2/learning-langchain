"""
1. Ensure docker is installed and running (https://docs.docker.com/get-docker/)
2. pip install -qU langchain_postgres
3. Run the following command to start the postgres container:
   
docker run \
    --name pgvector-container \
    -e POSTGRES_USER=langchain \
    -e POSTGRES_PASSWORD=langchain \
    -e POSTGRES_DB=langchain \
    -p 6024:5432 \
    -d pgvector/pgvector:pg16
4. Use the connection string below for the postgres container

"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()
from langchain_postgres.vectorstores import PGVector
from langchain_core.documents import Document
import uuid


# See docker command above to launch a postgres instance with pgvector enabled.
connection = "postgresql+psycopg://langchain:langchain@localhost:6024/langchain"

# Load the document, split it into chunks
raw_documents = TextLoader('./test.txt', encoding="utf-8").load()
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(raw_documents)

# Create embeddings for the documents
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GOOGLE_API_KEY"))

db = PGVector.from_documents(
    documents, embeddings_model, connection=connection)

results = db.similarity_search("query", k=4)

print(results)

print("Adding documents to the vector store")
ids = [str(uuid.uuid4()), str(uuid.uuid4())]
db.add_documents(
    [
        Document(
            page_content="there are cats in the pond",
            metadata={"location": "pond", "topic": "animals"},
        ),
        Document(
            page_content="ducks are also found in the pond",
            metadata={"location": "pond", "topic": "animals"},
        ),
    ],
    ids=ids,
)

print("Documents added successfully.\n Fetched documents count:",
      len(db.get_by_ids(ids)))

print("Deleting document with id", ids[1])
db.delete({"ids": ids})

print("Document deleted successfully.\n Fetched documents count:",
      len(db.get_by_ids(ids)))
