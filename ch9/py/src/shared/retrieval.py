from contextlib import contextmanager
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_core.runnables import RunnableConfig
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_chroma import Chroma
from supabase import create_client
import chromadb


from ingestion_graph.configuration import IndexConfiguration


def make_text_encoder(model: str) -> Embeddings:
    """Connect to the configured text encoder."""
    provider, model = model.split("/", maxsplit=1)
    if provider == "openai":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        # Use Google Gemini instead of OpenAI
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")


@contextmanager
def make_supabase_retriever(configuration: RunnableConfig, embedding_model: Embeddings):
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

    if not supabase_url or not supabase_key:
        raise ValueError(
            "Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env variables")

    client = create_client(supabase_url, supabase_key)
    vectorstore = SupabaseVectorStore(
        client=client, embedding=embedding_model, table_name="documents", query_name="match_documents")
    search_kwargs = configuration.search_kwargs
    yield vectorstore.as_retriever(search_kwargs=search_kwargs)


@contextmanager
def make_chroma_retriever(configuration: IndexConfiguration, embedding_model: Embeddings):
    client = chromadb.HttpClient(host='localhost', port=8000)

    vectorstore = Chroma(
        collection_name="documents",
        embedding_function=embedding_model,
        client=client
    )
    search_kwargs = configuration.search_kwargs
    search_filter = search_kwargs.setdefault("filter", {})
    yield vectorstore.as_retriever(search_kwargs=search_kwargs)


@contextmanager
def make_retriever(
    config: RunnableConfig,
):
    """Create a retriever for the agent, based on the current configuration."""
    configuration = IndexConfiguration.from_runnable_config(config)
    embedding_model = make_text_encoder(configuration.embedding_model)
    if configuration.retriever_provider == "supabase":
        with make_supabase_retriever(configuration, embedding_model) as retriever:
            yield retriever
    elif configuration.retriever_provider == "chroma":
        with make_chroma_retriever(configuration, embedding_model) as retriever:
            yield retriever
    else:
        raise ValueError(
            "Unrecognized retriever_provider in configuration. "
            f"Expected one of: {', '.join(Configuration.__annotations__['retriever_provider'].__args__)}\n"
            f"Got: {configuration.retriever_provider}"
        )
