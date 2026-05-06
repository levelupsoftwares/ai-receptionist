from ingest.ingest import ingest_pipeline #  chunks of all data
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from agent.config import settings


def get_embedding():
       return OpenAIEmbeddings(
        model= settings.EMBEDDING_MODEL,
        api_key=settings.OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1",

    )

def build_vectorstore(chunks):
    """Run only via ingest pipeline"""
 
    vector_store = Chroma.from_documents(
        documents= chunks,
        embedding= get_embedding(),
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name='2026-xPlumbers'
    )

    return vector_store


def load_vector_store():
    """"Used by agent at runtime -no rebuilding"""
    return Chroma(
        embedding_function=get_embedding(),
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name='2026-xPlumbers'
    )

# build_vectorstore(ingest_pipeline())    