# pipeline.py
from loader import file_loader
from chunker import chunk_documents

# Extract
raw_docs = file_loader()           # 1 doc per JSON file (raw JSON as text)

# Transform
chunks = chunk_documents(raw_docs) # N docs per file (clean text + metadata)

# print(chunks[6])


for c in chunks:
    print("\n===== CHUNK =====")
    print("Content:", c.page_content, "...")
    print("Metadata:", c.metadata)
