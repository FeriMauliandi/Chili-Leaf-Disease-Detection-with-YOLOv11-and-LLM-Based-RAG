---
title: ChiliCare AI
emoji: 🌶️
colorFrom: red
colorTo: yellow
sdk: docker
pinned: false
short_description: Deteksi Penyakit Daun Cabai berbasis YOLOv11 dan LLM
---

# ChiliCare AI
*(Anda bisa membiarkan isi README lama Anda di bawah garis pemisah ini...)*


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
```

## 🧪 Testing & CI/CD

Proyek ini telah dilengkapi dengan pengujian otomatis (*Unit Testing*) menggunakan `pytest` dan alur kerja CI/CD menggunakan **GitHub Actions**.

### Menjalankan Unit Test Lokal
```bash
pytest -v
```

### CI/CD Pipeline (.github/workflows/ci.yml)
Setiap kali ada `push` atau `pull request` ke *branch* `main` atau `master`, GitHub Actions akan menjalankan **CI/CD Pipeline** otomatis:

#### 1. Continuous Integration (CI)
* **Linting Kode**: Memeriksa kualitas kode dengan `ruff`.
* **Unit Testing**: Menjalankan seluruh pengujian unit di direktori `tests/` dan mengukur cakupan kode (*code coverage*).
* **Docker Build Verification**: Memastikan `Dockerfile` dapat di-build dengan sukses tanpa kesalahan dependensi.

#### 2. Continuous Deployment (CD)
* **Publish Docker Image ke GHCR**: Otomatis mem-build dan me-release image Docker produksi ke **GitHub Container Registry (GHCR)** (`ghcr.io/FeriMauliandi/chilicare-app:latest`).
* **Deploy ke Hugging Face Space**: Otomatis men-deploy dan me-refresh aplikasi ke **Hugging Face Space** (`feryms/chilicareAI`) secara otomatis saat terdapat perubahan pada branch `main`.

