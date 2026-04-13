import os
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Import prompt dari file terpisah yang baru dibuat
from src.chains.prompt import DISEASE_PROMPT_TEMPLATE

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0.4,
    max_tokens=1500
)

print("Memuat koneksi ke Database...")
embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")
vectorstore = Chroma(
    persist_directory="chroma_data", 
    embedding_function=embeddings,
    collection_name="chilicare_kb"
)

chain = DISEASE_PROMPT_TEMPLATE | llm

def generate_narrative(disease_name):
    print(f"Mencari data untuk label: {disease_name}...")
    
    results = vectorstore.similarity_search(
        query="berikan penjelasan lengkap", # dummy query karena kita sudah filter berdasarkan label
        k=1,
        filter={"label": disease_name}
    )

    if not results:
        return f"Data penyakit '{disease_name}' tidak ditemukan di database."

    retrieved_context = results[0].page_content

    print("Data ditemukan. Menghasilkan narasi dengan LLM...")

    response = chain.invoke({
        "disease_name": disease_name,
        "context": retrieved_context
    })
    
    return response.content