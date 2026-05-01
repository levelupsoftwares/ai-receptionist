#  loader that load the data from data/docs folder and add metadata

from langchain_community.document_loaders import JSONLoader,DirectoryLoader
from pathlib import Path

def file_loader():
    total_docs = []
    loader  = DirectoryLoader(
        path=Path(__file__).resolve().parents[1]/'data/docs',
        glob="**/*.json",
        loader_cls=JSONLoader,
        recursive=True,
        loader_kwargs={
            "jq_schema":".",
            "text_content":False
        }
    )
    doc = loader.lazy_load()

    # i have to extract the file name only from metadata to use as meta data   
    # {'source': '/home/usman/Desktop/ai-receptionist/data/docs/faqs.json', 'seq_num': 1} -> {'source': 'faqs', 'seq_num': 1}
    for page in doc:
        x  =Path(page.metadata['source']).stem 
        page.metadata['source']  = x
        # print(page.metadata)
        total_docs.append(page)
    
    return total_docs
    
print(file_loader())
