from ingest.ingest import ingest_pipeline #  chunks of all data
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from agent.config import settings

def build_vectorstore(chunks):
    embeddings = OpenAIEmbeddings(
        model= settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1",

    )
    vector_store = Chroma.from_documents(
        documents= chunks,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name='2026-xPlumbers'
    )

    return vector_store

build_vectorstore(ingest_pipeline())