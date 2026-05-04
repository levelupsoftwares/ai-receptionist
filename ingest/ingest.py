# pipeline.py
from ingest.loader import file_loader
from ingest.chunker import chunk_documents

def ingest_pipeline():

    # Extract
    raw_docs = file_loader()           # 1 doc per JSON file (raw JSON as text)

    # Transform
    chunks = chunk_documents(raw_docs) # N docs per file (clean text + metadata)

    return chunks

# print(chunks[6])


# for c in chunks:
#     print("\n===== CHUNK =====")
#     print("Content:", c.page_content, "...")
#     print("Metadata:", c.metadata)
