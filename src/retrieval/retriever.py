from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document

def get_retriever(vector_store, search_type="similarity", k=4, filter_label=None):
    print(f"Menyiapkan Hybrid Retriever (Vektor + BM25, Mengambil {k} dokumen)")
    
    search_kwargs = {"k": k}
    if filter_label:
        search_kwargs["filter"] = {"label": filter_label}
        
    vector_retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs=search_kwargs
    )
    
    where_clause = {"label": filter_label} if filter_label else None
    db_data = vector_store.get(where=where_clause)
    
    if not db_data or not db_data.get('documents'):
        print("Peringatan: Tidak ada dokumen untuk dibuatkan indeks BM25.")
        return vector_retriever
        
    docs = [
        Document(page_content=txt, metadata=meta or {}) 
        for txt, meta in zip(db_data['documents'], db_data.get('metadatas', []))
    ]
    
    # BM25 Retriever
    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = k
    
    hybrid_retriever = EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.5, 0.5]
    )
    
    return hybrid_retriever