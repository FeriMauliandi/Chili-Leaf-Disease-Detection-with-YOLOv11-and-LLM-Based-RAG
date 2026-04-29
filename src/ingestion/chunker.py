from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List

#   chunk_overlap: Jumlah karakter yang tumpang tindih antar potongan.
chunk_size = 1000
chunk_overlap = 200

def split_documents(documents: List[Document], chunk_size, chunk_overlap):
    print(f"Memulai proses pemotongan {len(documents)} dokumen...")
    
    # Inisialisasi splitter
    # Kita menggunakan karakter [\n\n, \n, " ", ""] sebagai prioritas pemisah
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"Berhasil memecah dokumen menjadi {len(chunks)} potongan teks.")
    return chunks