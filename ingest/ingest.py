# pipeline.py
import pickle
from ingest.loader import file_loader
from ingest.chunker import chunk_documents

def ingest_pipeline():

    # Extract
    raw_docs = file_loader()           # 1 doc per JSON file (raw JSON as text)

    # Transform
    chunks = chunk_documents(raw_docs) # N docs per file (clean text + metadata)

    return chunks
# store the chunks in disk with using pickle for the purpose to use it cache to get it for BM25 Retriever
with open('chunk.pkl','wb') as f:
    pickle.dump(ingest_pipeline(),f)

# print(chunks[6])


# for c in chunks:
#     print("\n===== CHUNK =====")
#     print("Content:", c.page_content, "...")
#     print("Metadata:", c.metadata)
