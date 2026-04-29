import sys
import os
from dotenv import load_dotenv

# Menambahkan root directory ke sys.path agar bisa import dari folder src
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(root_dir)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI # <- Import ini wajib ada untuk OpenRouter
from langchain_core.messages import SystemMessage
from src.ingestion.embedder import get_embedding_model # Menggunakan fungsi get_embedder yang kita bahas sebelumnya
from src.retrieval.vector_store import get_vector_store
from src.retrieval.retriever import get_retriever
from src.chains.prompt import get_rag_prompt

# Load environment variables (seperti OPENROUTER_API_KEY) dari file .env
load_dotenv()

def create_rag_chain():
    # 1. Setup Komponen Pencarian (Retriever)
    vs = get_vector_store()
    retriever = get_retriever(vs) # Fungsi ini dari retriever.py yang sudah di-set k=2
    
    # 2. Setup Prompt & LLM
    prompt = get_rag_prompt()
    
    llm = ChatOpenAI(
        model="nvidia/nemotron-3-nano-30b-a3b:free", 
        temperature=0.2,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"), 
        openai_api_base="https://openrouter.ai/api/v1",
    ) 
    
    # 3. Fungsi Interceptor untuk Debugging
    def format_docs(docs):
        # ==========================================
        # INTERCEPTOR: Print metadata ke Terminal VS Code
        # ==========================================
        print("\n" + "▼"*50)
        print("🔍 [DEBUG] DOKUMEN YANG DITARIK RETRIEVER:")
        for i, doc in enumerate(docs):
            # Mengambil informasi 'label' (penyakit) dari metadata db_setup.py
            sumber = doc.metadata.get('label', 'Sumber tidak diketahui')
            
            print(f"  [{i+1}] Topik/Label: {sumber}")
            # print(f"      Teks: {doc.page_content[:75]}...") 
        print("▲"*50 + "\n")
        # ==========================================
        
        # Gabungkan teks untuk dikirim ke LLM
        return "\n\n".join(doc.page_content for doc in docs)
        
    # 4. Rangkai menjadi Chain (LCEL)
    rag_chain = (
        # Ubah "question" menjadi "input" agar cocok dengan prompt Anda
        {"context": retriever | format_docs, "input": RunnablePassthrough()} 
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# ======= Blok testing =========
if __name__ == "__main__":
    chain = create_rag_chain()
    
    # Menggunakan pertanyaan seputar cabai agar LLM bisa mengambil dari ChromaDB Anda
    pertanyaan = "Bagaimana cara menangani penyakit antraknosa (patek) pada tanaman cabai?"
    print(f"\nUser: {pertanyaan}")
    print("AI sedang berpikir (memproses via OpenRouter)...\n")
    
    try:
        jawaban = chain.invoke(pertanyaan)
        print("=== JAWABAN RAG ===")
        print(jawaban)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")