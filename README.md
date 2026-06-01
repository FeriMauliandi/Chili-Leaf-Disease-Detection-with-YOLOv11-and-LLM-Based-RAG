# ChiliCare: Chili Leaf Disease Detection with YOLOv11 and RAG

**ChiliCare** adalah sebuah aplikasi web AI berarsitektur *dual-pipeline* yang dirancang untuk manajemen kesehatan tanaman cabai. Sistem ini mengintegrasikan model *Computer Vision* (**YOLOv11**) untuk deteksi penyakit secara visual dan ekosistem *Large Language Models* (LLM) berbasis **Retrieval-Augmented Generation (RAG)** untuk memberikan diagnosis, rekomendasi penanganan, serta asisten virtual interaktif.

## Fitur Utama

- **Sistem Deteksi Penyakit (Upload-and-Predict)**
  Menggunakan model deteksi objek **YOLOv11** untuk mengidentifikasi area daun cabai yang terinfeksi secara akurat.

- **Diagnosis Berbasis RAG (Vision-to-Text)**
  Hasil deteksi *bounding box* dari YOLO diproses lebih lanjut oleh LLM menggunakan mekanisme RAG terstruktur untuk memberikan penjelasan penyakit dan rekomendasi penanganan secara otomatis.

- **Chatbot Pakar Percabaian (Text-to-Text)**
  Asisten virtual interaktif yang berjalan di *pipeline* terpisah menggunakan LangChain dan ChromaDB untuk menjawab pertanyaan spesifik seputar perawatan dan penyakit tanaman cabai.

- **Antarmuka Web Interaktif**
  Dibangun menggunakan **Streamlit** (`app.py`) untuk menghadirkan antarmuka pengguna yang bersih dan mudah digunakan.

- **Siap Deployment (Dockerized)**
  Proyek ini telah dikonfigurasi dengan Docker, memastikan sistem berjalan konsisten di berbagai lingkungan tanpa masalah dependensi.

## Teknologi yang Digunakan

- **Computer Vision:** YOLOv11 (Ultralytics), OpenCV
- **AI & LLM Ecosystem:** Python, LangChain, ChromaDB
- **Web Framework:** Streamlit
- **Deployment & Ops:** Docker

## Struktur File Utama

- `app.py`: Skrip utama untuk menjalankan antarmuka web Streamlit dan orkestrasi model.
- `train_yolo11_chili_leaf_disease_detection.ipynb`: Notebook komprehensif yang berisi *pipeline* prapemrosesan data, augmentasi, pelatihan, dan evaluasi model YOLOv11.
- `data.json`: Basis pengetahuan (konteks, label, referensi penanganan) yang digunakan oleh vektor database untuk mekanisme RAG.

## Cara Menjalankan Proyek

### Opsi 1: Menggunakan Docker (Direkomendasikan)
Pastikan Docker sudah terinstal di sistem Anda, lalu jalankan perintah berikut:

```bash
# Build image docker
docker build -t chilicare-app .

# Jalankan container
docker run -p 8501:8501 chilicare-app
