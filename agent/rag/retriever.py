from agent.rag.embedder import load_vector_store
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from agent.config import settings
import pickle

chunks_path = settings.BASE_DIR/'data'/'chunk.pkl'
_retriever = None

def build_retriever():
    
    vector_store = load_vector_store()
    # Dense Search
    dense_search = vector_store.as_retriever(
        search_type='mmr',
        search_kwargs={'k':2,'fetch_k':10}
    )

    # Sparse Search
    # get chunks from pickle which is cache of the doc-chunks 
    with open(chunks_path,'rb') as cache_chunks:
        chunk_loaded = pickle.load(cache_chunks)


    sparse_search = BM25Retriever.from_documents(
        documents=chunk_loaded,
    )
    sparse_search.k = 2
 
    return EnsembleRetriever(
        retrievers= [dense_search,sparse_search],
        weights=[0.5,0.5]
    )


def get_retriever():
    global _retriever
    if _retriever is None:
        _retriever = build_retriever()
    return _retriever

    
def retriever_context(query: str)->str:
    retriever = get_retriever()
    docs =  retriever.invoke(query)
    top_docs =  docs[:2]
    return "\n\n".join(
        doc.page_content for doc in top_docs
    )



