import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Inisialisasi LLM (Tetap sama)
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0.6,
    max_tokens=1500
)

# 2. Koneksi ke ChromaDB Lokal
print("Memuat koneksi ke Database...")
embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")
vectorstore = Chroma(
    persist_directory="chroma_data", # Pastikan nama foldernya sama dengan di db_setup.py
    embedding_function=embeddings,
    collection_name="chilicare_kb"
)

# 3. Setup Prompt Template (Lebih Ringkas)
# Kita hanya butuh 'context' karena isi penyebab/gejala sudah dirakit oleh db_setup.py
prompt_template = PromptTemplate(
    input_variables=["disease_name", "context"],
    template="""
Anda adalah penyuluh pertanian cabai.

Gunakan HANYA informasi referensi berikut. Jangan menambahkan fakta baru di luar referensi.

--- REFERENSI DATABASE ---
{context}
--------------------------

Tugas:
Jelaskan tentang kondisi/penyakit "{disease_name}" berdasarkan referensi di atas.
Gunakan bahasa yang sederhana, ramah, dan mudah dipahami oleh petani cabai.
Jika kondisinya adalah "Sehat", berikan apresiasi dan jelaskan bahwa tanaman dalam kondisi prima(generate jika label gambar output adalah "sehat").
"""
)

# 4. Buat Chain LCEL
chain = prompt_template | llm

# 5. Fungsi Generate Narrative Terintegrasi RAG
def generate_narrative(disease_name):
    print(f"Mencari data untuk label: {disease_name}...")
    
    # RETRIEVAL: Mengambil data dari ChromaDB menggunakan Metadata Filter (Jalur YOLO)
    # Ini memastikan data yang ditarik 100% akurat sesuai label
    results = vectorstore.similarity_search(
        query="berikan penjelasan lengkap", # Query dummy karena kita mengandalkan filter
        k=1,
        filter={"label": disease_name}
    )

    if not results:
        return f"⚠️ Data penyakit '{disease_name}' tidak ditemukan di database."

    # Ambil teks referensi utuh dari hasil retrieval
    retrieved_context = results[0].page_content

    print("Data ditemukan. Menghasilkan narasi dengan LLM...")
    # GENERATION: Kirim konteks dan nama penyakit ke LLM
    response = chain.invoke({
        "disease_name": disease_name,
        "context": retrieved_context
    })
    
    return response.content

# --- TEST SCRIPT ---
if __name__ == "__main__":
    # Pastikan OPENROUTER_API_KEY sudah tersetting di environment variables kamu
    # Contoh penggunaan dari hasil output YOLO
    label_yolo = "Keriting" 
    hasil = generate_narrative(label_yolo)
    
    print("\n=== HASIL GENERATE ===")
    print(hasil)