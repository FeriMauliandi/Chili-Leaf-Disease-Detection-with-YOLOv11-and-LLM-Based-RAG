from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_DB_DIR = "chroma_data"
COLLECTION_NAME = "chilicare_kb"

def get_embedder():
    # Wajib sama persis dengan yang ada di db_setup.py
    return HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")

def get_vector_store():
    embedder = get_embedder()
    # Memuat database Chroma yang sudah dibuat oleh db_setup.py
    return Chroma(
        persist_directory=CHROMA_DB_DIR, 
        embedding_function=embedder,
        collection_name=COLLECTION_NAME
    )