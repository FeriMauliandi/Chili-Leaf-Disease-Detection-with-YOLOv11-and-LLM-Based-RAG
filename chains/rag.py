import json
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 1. Inisialisasi LLM
llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    temperature=0.6,
    max_tokens=1200
)

def retrieve_disease_info(disease_name):
    with open("data/data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(disease_name)

# 2. Setup Prompt Template
prompt_template = PromptTemplate(
    input_variables=["disease_name", "penyebab", "gejala", "penanganan", "pencegahan"],
    template="""
Anda adalah penyuluh pertanian cabai.

Gunakan HANYA informasi berikut.
Jangan menambahkan fakta baru.

Nama penyakit: {disease_name}

Penyebab:
- {penyebab}

Gejala:
- {gejala}

Penanganan:
- {penanganan}

Pencegahan:
- {pencegahan}

Gunakan bahasa sederhana untuk petani cabai.
Jika penyakit adalah sehat, jelaskan bahwa daun dalam kondisi sehat.
"""
)

# 3. Gunakan LCEL (LangChain Expression Language) sebagai pengganti LLMChain
chain = prompt_template | llm

def generate_narrative(disease_name):
    info = retrieve_disease_info(disease_name)
    if not info:
        return "⚠️ Data penyakit tidak ditemukan."

    # 4. Gunakan .invoke() dan ambil kontennya
    response = chain.invoke({
        "disease_name": disease_name,
        "penyebab": "; ".join(info["penyebab"]),
        "gejala": "; ".join(info["gejala"]),
        "penanganan": "; ".join(info["penanganan"]),
        "pencegahan": "; ".join(info["pencegahan"]),
    })
    
    return response.content