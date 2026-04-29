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

    print("Converting nested JSON data into LangChain Document format")
    documents = []
    
    for label, details in chili_data.items():
        teks_gabungan = f"Penyakit/Kondisi: {label}\n"
        
        if details.get("penyebab"):
            teks_gabungan += "Penyebab:\n- " + "\n- ".join(details["penyebab"]) + "\n"
        
        if details.get("gejala"):
            teks_gabungan += "Gejala:\n- " + "\n- ".join(details["gejala"]) + "\n"
            
        if details.get("penanganan"):
            teks_gabungan += "Penanganan:\n- " + "\n- ".join(details["penanganan"]) + "\n"
            
        if details.get("pencegahan"):
            teks_gabungan += "Pencegahan:\n- " + "\n- ".join(details["pencegahan"]) + "\n"

        doc = Document(
            page_content=teks_gabungan,
            metadata={"label": label}
        )
        documents.append(doc)

    # 4. Setup Embedding Model
    print("Memuat Embedding Model")
    embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")

    # 5. Simpan ke ChromaDB via LangChain
    print("Menyimpan data ke ChromaDB")
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR,
        collection_name="chilicare_kb"
    )
    print(f"Berhasil! Database tersimpan di folder: {CHROMA_DB_DIR}\n")


if __name__ == "__main__":
    main()