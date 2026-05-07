from ingest.ingest import ingest_pipeline #  chunks of all data
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from agent.config import settings


_embeddings = None
_vector_store = None

def get_embedding():
       global _embeddings
       if _embeddings is None:
            _embeddings = OpenAIEmbeddings(
                model= settings.EMBEDDING_MODEL,
                api_key=settings.OPENAI_API_KEY,
                base_url="https://openrouter.ai/api/v1",
    )
       return _embeddings

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
    global _vector_store
    if _vector_store is None:
        _vector_store = Chroma(
        embedding_function=get_embedding(),
        persist_directory=settings.CHROMA_DB_DIR,
        collection_name='2026-xPlumbers'
    )
    return _vector_store

# build_vectorstore(ingest_pipeline())    