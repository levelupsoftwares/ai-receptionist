import json
from langchain_core.documents import Document

def chunk_documents(documents: list[Document]) -> list[Document]:
    """
    Splits file-level Documents (each containing a full JSON file)
    into individual chunk-level Documents with rich metadata.
    """
    chunked_docs = []

    for doc in documents:
        # 1. Parse the JSON that loader dumped into page_content
        try:
            data = json.loads(doc.page_content) if isinstance(doc.page_content, str) else doc.page_content
        except (json.JSONDecodeError, TypeError):
            continue  # skip corrupted files

        # 2. Base metadata from the JSON envelope + loader's filename stem
        base_meta = {
            "source_domain": data.get("source_domain"),
            "last_crawled": data.get("last_crawled"),
            "file_source": doc.metadata.get("source"),   # "faqs", "policies", etc.
        }

        # 3. Explode each inner chunk into its own Document
        for chunk in data.get("chunks", []):
            content = chunk.get("content", "").strip()
            if not content:
                continue

            metadata = {
                **base_meta,
                "chunk_id": chunk.get("id"),
                "title": chunk.get("title"),
                "category": chunk.get("category"),
                "source_url": chunk.get("source_url"),
                "keywords": chunk.get("keywords", []),
            }

            chunked_docs.append(Document(
                page_content=content,
                metadata=metadata
            ))

    return chunked_docs