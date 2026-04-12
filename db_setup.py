import json
import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

JSON_FILE_PATH = "data/data.json"
CHROMA_DB_DIR = "chroma_data"

def main():
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: File {JSON_FILE_PATH} not found.")
        return
    
    print("Reading JSON data...")
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as f:
        chili_data = json.load(f)

    # 3. Konversi ke Format Document LangChain
    print("Converting nested JSON data into LangChain Document format")
    documents = []
    
    for label, details in chili_data.items():
        teks_gabungan = f"Penyakit/Kondisi: {label}\n"
        
        # Mengecek apakah list ada isinya, lalu digabung dengan newline
        if details.get("penyebab"):
            teks_gabungan += "Penyebab:\n- " + "\n- ".join(details["penyebab"]) + "\n"
        
        if details.get("gejala"):
            teks_gabungan += "Gejala:\n- " + "\n- ".join(details["gejala"]) + "\n"
            
        if details.get("penanganan"):
            teks_gabungan += "Penanganan:\n- " + "\n- ".join(details["penanganan"]) + "\n"
            
        if details.get("pencegahan"):
            teks_gabungan += "Pencegahan:\n- " + "\n- ".join(details["pencegahan"]) + "\n"

        # Membungkus teks rakitan dan metadata (label yolo)
        doc = Document(
            page_content=teks_gabungan,
            metadata={"label": label}
        )
        documents.append(doc)

    # 4. Setup Embedding Model
    print("Memuat Embedding Model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")

    # 5. Simpan ke ChromaDB via LangChain
    print("Menyimpan data ke ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name="chilicare_kb"
    )
    print(f"Berhasil! Database tersimpan di folder: {CHROMA_DB_DIR}\n")

    # ==========================================
    # --- TESTING HYBRID RETRIEVAL LANGCHAIN ---
    # ==========================================
    print("--- UJI COBA RETRIEVAL (LANGCHAIN) ---")
    
    # Tes A: Jalur YOLO (Metadata Filter)
    test_label = "Bercak" # Menguji label Bercak
    print(f"\n[JALUR YOLO] Mencari data dengan filter label: '{test_label}'")
    
    yolo_results = vectorstore.similarity_search(
        query="berikan penjelasan lengkap", 
        k=1,
        filter={"label": test_label} 
    )
    if yolo_results:
        print("✅ Ditemukan Data RAG (Cuplikan):")
        # Print 200 karakter pertama agar terminal tidak terlalu penuh
        print(f"{yolo_results[0].page_content[:200]}...") 

    # Tes B: Jalur Teks/Chat (Semantic Similarity Search)
    test_query = "daunnya melengkung ke atas seperti mangkuk dan kaku"
    print(f"\n[JALUR TEKS] User bertanya: '{test_query}'")
    
    chat_results = vectorstore.similarity_search(query=test_query, k=1)
    if chat_results:
        label_terdeteksi = chat_results[0].metadata['label']
        print(f"✅ Sistem menduga ini penyakit: '{label_terdeteksi}'")
        print("📄 Cuplikan Penjelasan:")
        print(f"{chat_results[0].page_content[:200]}...")

if __name__ == "__main__":
    main()