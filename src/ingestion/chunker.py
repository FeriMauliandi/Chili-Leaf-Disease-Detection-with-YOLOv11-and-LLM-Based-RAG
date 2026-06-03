from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_core.documents import Document
from typing import List
from src.ingestion.embedder import get_embedding_model 

def split_documents(documents: List[Document], chunk_size, chunk_overlap):
    print(f"Memulai proses pemotongan {len(documents)} dokumen...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"Berhasil memecah dokumen menjadi {len(chunks)} potongan teks.")
    return chunks

# def split_documents_semantically(documents: List[Document]):
#     print(f"Memulai analisis semantik pada {len(documents)} dokumen")
    
#     embeddings = get_embedding_model()
    
#     # Inisialisasi Semantic Chunker
#     semantic_splitter = SemanticChunker(
#         embeddings, 
#         breakpoint_threshold_type="percentile"
#     )
    
#     chunks = semantic_splitter.split_documents(documents)
#     return chunks