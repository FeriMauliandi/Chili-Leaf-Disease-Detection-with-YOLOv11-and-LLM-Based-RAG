import streamlit as st
import requests
from PIL import Image
import io
import base64

# URL untuk kedua endpoint FastAPI
# API_DETECT_URL = "http://localhost:8000/detect"
# API_ASK_URL = "http://localhost:8000/ask"

API_DETECT_URL = "http://backend:8000/detect"
API_ASK_URL = "http://backend:8000/ask"

st.set_page_config(page_title="ChiliCare AI", page_icon="🌶️", layout="centered")

# === MEMBUAT SIDEBAR NAVIGASI ===
st.sidebar.title("🌶️ Menu ChiliCare")
st.sidebar.markdown("Pilih fitur yang ingin Anda gunakan:")
menu = st.sidebar.radio(
    "====",
    ["📷 Deteksi Penyakit (Gambar)", "🤖 Chatbot (Teks)"]
)

# === HALAMAN 1: DETEKSI PENYAKIT (GAMBAR) ===
if menu == "📷 Deteksi Penyakit (Gambar)":
    st.title("🌶️🌿 Deteksi Penyakit Daun Cabai")
    st.write("Unggah foto daun cabai yang sakit untuk mendapatkan diagnosis dan solusinya.")
    
    uploaded_file = st.file_uploader("Unggah gambar daun cabai anda", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)
       # st.image(original_image, caption="Gambar yang Diupload", use_container_width=True)

        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
        try:
            with st.spinner("Memproses gambar dengan YOLOv11..."):
                response = requests.post(API_DETECT_URL, files=files)
                
            if response.status_code == 200:
                data = response.json()
                    
                if "image_base64" in data:
                    image_bytes = base64.b64decode(data["image_base64"])
                    annotated_image = Image.open(io.BytesIO(image_bytes))
                    st.image(annotated_image, caption="Hasil Analisis YOLO", use_container_width=True)

                st.subheader("📋 Hasil Diagnosis: ")
                if data.get("total_detections", 0) > 0:
                    for item in data["results"]:
                        st.markdown(f"### 🦠 {item['class']} (Keyakinan: {item['confidence']:.0%})")
                        st.info(f"**Saran Penanganan:**\n\n{item['narrative']}")
                else:
                    st.success("Tidak ada penyakit yang terdeteksi. Daun tampak sehat!")
            else:
                st.error(f"Gagal memproses gambar. Error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Gagal terhubung ke server FastAPI. Pastikan backend sudah berjalan.")

# === HALAMAN 2: TANYA AHLI (TEKS) ===
elif menu == "🤖 Chatbot (Teks)":
    st.title("🤖 Chatbot Ahli Cabai")
    st.write("Tanyakan seputar perawatan, penyakit, atau pupuk cabai. Saya siap membantu!")
    
    # 1. Inisialisasi memori obrolan (session state)
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 2. Tampilkan riwayat chat sebelumnya agar tidak hilang saat halaman direfresh
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 3. Kolom input untuk user menggunakan gaya chat
    if prompt := st.chat_input("Tulis pertanyaan Anda di sini... (misal: Kapan waktu panen cabai?)"):
        
        # Tampilkan pesan user di layar
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Simpan pesan user ke memori
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Siapkan tempat untuk jawaban AI
        with st.chat_message("assistant"):
            with st.spinner("Berpikir dan mencari referensi..."):
                try:
                    # KITA KIRIM REQUEST KE FASTAPI (Bukan panggil chain lokal)
                    payload = {"question": prompt}
                    response = requests.post(API_ASK_URL, json=payload)
                    
                    if response.status_code == 200:
                        data = response.json()
                        jawaban = data["answer"]
                        
                        # Tampilkan jawaban dari FastAPI/LLM
                        st.markdown(jawaban)
                        
                        # Simpan jawaban ke memori
                        st.session_state.messages.append({"role": "assistant", "content": jawaban})
                    else:
                        error_msg = f"Gagal mendapatkan jawaban. Error: {response.status_code}"
                        st.error(error_msg)
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        
                except requests.exceptions.ConnectionError:
                    error_msg = "Gagal terhubung ke server FastAPI. Pastikan backend sudah berjalan."
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

st.sidebar.markdown("---")

st.sidebar.markdown("""
    # Spesifikasi Model AI
    **1. Vision (Deteksi Penyakit)**
    * Model: `YOLOv11s` (Small)
    * Framework: `Ultralytics`
    
    **2. Retrieval-Augmented Generation (RAG)**
    * Vector Database: `ChromaDB`
    * Embedding: `Qwen3-Embedding-0.6B`
    
    **3. Large Language Model (LLM)**
    * Model: `Nvidia Nemotron-3 120B`
    * Provider: `OpenRouter`
    """)

st.sidebar.markdown("---")

st.sidebar.caption("© 2026 ChiliCare AI Engineer Portfolio")