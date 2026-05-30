import sys
import os
from dotenv import load_dotenv

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(root_dir)

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI 
from langchain_core.messages import SystemMessage
from langchain_classic.retrievers import MultiQueryRetriever
from src.ingestion.embedder import get_embedding_model 
from src.retrieval.vector_store import get_vector_store
from src.retrieval.retriever import get_retriever
from src.chains.prompt import get_rag_prompt

load_dotenv()

def create_rag_chain():
    llm = ChatOpenAI(
        model="nvidia/nemotron-3-nano-30b-a3b:free", 
        temperature=0.2,
        openai_api_key=os.getenv("OPENROUTER_API_KEY"), 
        openai_api_base="https://openrouter.ai/api/v1",
    ) 
    
    vs = get_vector_store()
    base_retriever = get_retriever(vs, search_type="similarity", k=3) # Mengambil 3 chunks teratas
    
    # 3. REFACTOR: Bungkus menjadi Multi-Query Retriever
    # LLM akan otomatis membuat ~3 variasi pertanyaan alternatif dari pertanyaan user
    # untuk memastikan dokumen di ChromaDB terambil dengan lebih akurat secara semantik.
    retriever = MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm
    )
    
    # 4. Setup Prompt
    prompt = get_rag_prompt()
    
    # 5. Fungsi Interceptor untuk Debugging di Terminal
    def format_docs(docs):
        # ==========================================
        # INTERCEPTOR: Print metadata ke Terminal
        # ==========================================
        print("\n" + "▼"*50)
        print("🔍 [DEBUG] DOKUMEN YANG DITARIK MULTI-QUERY RETRIEVER:")
        for i, doc in enumerate(docs):
            sumber = doc.metadata.get('label', 'Sumber tidak diketahui')
            print(f"  [{i+1}] Topik/Label: {sumber}")
        print("▲"*50 + "\n")
        # ==========================================
        
        # Gabungkan teks dokumen yang berhasil dikumpulkan dari semua query alternatif
        return "\n\n".join(doc.page_content for doc in docs)
        
    # 6. Rangkai menjadi Chain (LCEL)
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()} 
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# ======= Blok testing =========
if __name__ == "__main__":
    chain = create_rag_chain()
    
    pertanyaan = "Bagaimana cara menangani penyakit antraknosa (patek) pada tanaman cabai?"
    print(f"\nUser: {pertanyaan}")
    print("AI sedang berpikir (memproses via OpenRouter)...\n")
    
    try:
        jawaban = chain.invoke(pertanyaan)
        print("=== JAWABAN RAG ===")
        print(jawaban)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")