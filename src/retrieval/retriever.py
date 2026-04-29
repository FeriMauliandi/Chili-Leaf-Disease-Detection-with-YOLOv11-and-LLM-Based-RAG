def get_retriever(vector_store, search_type="similarity", k=4):
    """
    Mengubah Vector Store menjadi objek Retriever untuk mencari dokumen relevan.
    
    Args:
        vector_store: Objek ChromaDB yang sudah dimuat.
        search_type: Tipe pencarian ('similarity' atau 'mmr').
        k: Jumlah potongan dokumen (chunks) teratas yang ingin diambil.
    """
    print(f"Menyiapkan Retriever (Tipe: {search_type}, Mengambil {k} dokumen)")
    
    retriever = vector_store.as_retriever(
        search_type=search_type,
        search_kwargs={"k": k}
    )
    
    return retriever