from langchain_core.prompts import PromptTemplate

def get_rag_prompt():
    template = """Anda adalah asisten AI spesialis pertanian cabai.
    Gunakan konteks berikut untuk menjawab pertanyaan pengguna.
    Jika jawabannya tidak ada di dalam konteks, katakan dengan jujur bahwa Anda tidak tahu. Jangan mengarang informasi.

    Konteks: {context}

    Pertanyaan: {input}

    Jawaban yang detail dan ramah:"""
    
    return PromptTemplate.from_template(template)


DISEASE_PROMPT_TEMPLATE = PromptTemplate(
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
Jika kondisinya adalah "Sehat", berikan apresiasi dan jelaskan bahwa tanaman dalam kondisi sehat (jangan jawab jika hasilnya bukan "sehat").
"""
)

