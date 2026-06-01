import os
import sys
root_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(root_dir)

from src.ingestion.loader import load_data
from src.ingestion.chunker import split_documents
from src.retrieval.vector_store import get_vector_store

SOURCES = [
    "https://www.dgwfertilizer.co.id/8-hama-dan-penyakit-penting-pada-tanaman-cabai/",
    "https://mitrabertani.com/artikel/detail/Budidaya-Cabai-Sederhana-tapi-Penting-Cara-Tepat-Tanam-Cabai",
    "https://digitani.ipb.ac.id/bagaimana-langkah-langkah-budidaya-cabai/",
    "data/cabai.pdf"
]

def run_ingestion_pipeline():
    print("Memulai Data Ingestion Pipeline\n")
    all_chunks = []
    
    for source in SOURCES:
        try:
            raw_docs = load_data(source)
            chunks = split_documents(raw_docs, chunk_size=1000, chunk_overlap=150)
            all_chunks.extend(chunks)
            print(f"Berhasil memproses: {source} ({len(chunks)} chunks)")
        except Exception as e:
            print(f"Gagal memproses {source}: {e}")
            
    if all_chunks:
        print(f"\nMenyiapkan model embedding dan menyimpan {len(all_chunks)} chunks ke ChromaDB...")
        
        db = get_vector_store()
        
        db.add_documents(all_chunks)
        
        print("\nSelesai! Semua data web telah masuk ke database dan siap digunakan oleh API/Streamlit.")
    else:
        print("\nTidak ada data yang berhasil diproses.")

if __name__ == "__main__":
    run_ingestion_pipeline()