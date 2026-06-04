<div align="center">

# 🌶️ ChiliCare AI

### Chili Leaf Disease Detection with YOLOv11 & RAG Pipeline

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)](https://python.org)
[![YOLOv11](https://img.shields.io/badge/YOLOv11-Ultralytics-orange)](https://ultralytics.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green)](https://langchain.com)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-blue?logo=docker)](https://docker.com)

<!-- 📸 [IMAGE: Demo GIF / screenshot aplikasi — tampilkan halaman deteksi penyakit sebelah kiri dan chatbot sebelah kanan, format GIF lebih direkomendasikan] -->

</div>

---

## 📖 Tentang Proyek

**ChiliCare** adalah aplikasi web AI berarsitektur *dual-pipeline* untuk manajemen kesehatan tanaman cabai. Sistem ini menggabungkan dua domain AI secara end-to-end:

- **Computer Vision** → YOLOv11 mendeteksi area daun yang terinfeksi secara visual
- **LLM + RAG** → Mengubah hasil deteksi menjadi diagnosis naratif dan rekomendasi penanganan yang kontekstual

Proyek ini dibangun sebagai Tugas Akhir sekaligus portofolio AI Engineering, dengan fokus pada integrasi pipeline CV dan LLM dalam satu sistem yang dapat di-deploy.

---

## 🏗️ Arsitektur Sistem

<!-- 📸 [IMAGE: Diagram arsitektur sistem — tampilkan dua pipeline: (1) Vision Pipeline: User Upload → YOLOv11 → Bounding Box + Label → RAG → LLM → Diagnosis Naratif, dan (2) Chat Pipeline: User Input → MultiQueryRetriever → CrossEncoder Reranker → LLM → Jawaban. Bisa dibuat dengan draw.io, Mermaid, atau Excalidraw] -->

### Pipeline 1: Vision Diagnosis (Image → Text)

```
Gambar Daun → YOLOv11 Inference → Detected Label + Confidence
                                         ↓
                              RAG dengan Metadata Filter (by label)
                                         ↓
                              LLM (Groq) → Narasi Diagnosis + Rekomendasi
```

### Pipeline 2: Expert Chatbot (Text → Text)

```
Pertanyaan User → MultiQueryRetriever (LangChain)
                         ↓
              ChromaDB Similarity Search (top-5)
                         ↓
           CrossEncoder Reranker (BAAI/bge-reranker-base, top-3)
                         ↓
              LLM (Groq) → Jawaban Kontekstual
```

> **Desain keputusan:** Pipeline chatbot menggunakan full retrieval stack (MultiQuery + Reranking) karena query bersifat open-ended. Pipeline vision menggunakan metadata-filtered RAG karena label penyakit sudah diketahui dari output YOLO, sehingga retrieval presisi lebih efisien.

---

## ✨ Fitur Utama

| Fitur | Deskripsi | Teknologi |
|-------|-----------|-----------|
| 🔍 **Deteksi Penyakit** | Upload gambar daun, sistem mendeteksi area terinfeksi dengan bounding box | YOLOv11, OpenCV |
| 📋 **Diagnosis Otomatis** | Hasil deteksi dikonversi menjadi penjelasan penyakit dan saran penanganan | RAG, LangChain, Groq |
| 🤖 **Chatbot Pakar** | Asisten interaktif untuk tanya jawab seputar perawatan dan penyakit cabai | MultiQuery RAG, CrossEncoder Reranker |
| 🐳 **Siap Deploy** | Dikonfigurasi dengan Docker dan docker-compose untuk deployment yang konsisten | Docker, FastAPI |

---

## 📊 Performa Model YOLOv11

<!-- 📸 [IMAGE: Confusion matrix dari hasil training — export dari Ultralytics training output folder (runs/detect/train/confusion_matrix.png)] -->

<!-- 📸 [IMAGE: Grafik training curves — loss curve dan mAP curve (runs/detect/train/results.png)] -->

| Metrik | Nilai |
|--------|-------|
| mAP@50 | <!-- isi dari hasil training Anda --> |
| Precision | <!-- isi dari hasil training Anda --> |
| Recall | <!-- isi dari hasil training Anda --> |
| Dataset | Roboflow — Chili Leaf Disease |
| Epochs | <!-- isi jumlah epoch --> |
| Model Variant | YOLOv11s (Small) |

---

## 🔬 Detail RAG Pipeline

### Knowledge Base

Sistem menggunakan dua sumber pengetahuan yang dikombinasikan:

| Sumber | Format | Konten |
|--------|--------|--------|
| `data/data.json` | JSON terstruktur | Label penyakit, gejala, penyebab, penanganan, pencegahan |
| Web scraping (3 URL) | Teks tidak terstruktur | Artikel budidaya cabai dari sumber agrikultur |
| PDF (3 file) | Dokumen | Referensi penyakit dan budidaya cabai rawit |

### Konfigurasi Retrieval

```
Embedding Model : Qwen/Qwen3-Embedding-0.6B
Vector Database : ChromaDB (persistent)
Chunk Size      : 1000 tokens | Overlap: 200 tokens
Search Type     : Similarity (top-5)
Reranker        : BAAI/bge-reranker-base (top-3)
LLM             : Groq — gpt-oss-20b
```

---

## 🛠️ Teknologi yang Digunakan

```
Computer Vision  : YOLOv11 (Ultralytics), OpenCV
LLM Ecosystem    : LangChain, ChromaDB, HuggingFace
LLM Inference    : Groq API
Reranking        : BAAI/bge-reranker-base (CrossEncoder)
Backend          : FastAPI
Frontend         : Streamlit
Deployment       : Docker, docker-compose
```

---

## 🚀 Cara Menjalankan

### Prasyarat

- Docker & docker-compose terinstal
- API key Groq (daftar di [console.groq.com](https://console.groq.com))

### Langkah 1: Clone Repository

```bash
git clone https://github.com/FeriMauliandi/Chili-Leaf-Disease-Detection-with-YOLOv11-and-LLM-Based-RAG.git
cd Chili-Leaf-Disease-Detection-with-YOLOv11-and-LLM-Based-RAG
```

### Langkah 2: Konfigurasi Environment

```bash
cp .env.example .env
# Edit .env dan isi GROQ_API_KEY dengan API key Anda
```

### Langkah 3: Build & Jalankan dengan Docker (Direkomendasikan)

```bash
docker-compose up --build
```

Akses aplikasi di: **http://localhost:8501**

### Langkah 4 (Opsional): Setup Knowledge Base Secara Manual

Jika ingin rebuild vector database dari awal:

```bash
# Setup dari data.json (structured)
python db_setup.py

# Atau dari web + PDF (multi-source)
python ingest.py
```

---

## 📁 Struktur Proyek

```
chilicare-ai/
├── app.py                  # Streamlit frontend & orkestrasi UI
├── ingest.py               # Multi-source ingestion pipeline (web + PDF)
├── db_setup.py             # Structured knowledge base setup (JSON)
├── backend/
│   └── main.py             # FastAPI endpoints (/detect, /ask)
├── src/
│   ├── ingestion/
│   │   ├── loader.py       # Document loader (URL & PDF)
│   │   └── chunker.py      # Semantic text chunker
│   ├── retrieval/
│   │   ├── vector_store.py # ChromaDB interface
│   │   └── retriever.py    # Retriever dengan metadata filter
│   └── chains/
│       ├── chain.py        # Full RAG chain (MultiQuery + Reranker)
│       ├── rag.py          # Vision RAG chain (label-filtered)
│       └── prompt.py       # Prompt templates
├── model/                  # YOLOv11 weights (.pt)
├── data/                   # Knowledge base files
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

---

## 🖼️ Screenshot Aplikasi

<!-- 📸 [IMAGE: Screenshot halaman "Deteksi Penyakit" — tampilkan contoh gambar daun yang sudah ter-annotate dengan bounding box YOLO + teks diagnosis di bawahnya] -->

<!-- 📸 [IMAGE: Screenshot halaman "Chatbot Pakar" — tampilkan contoh percakapan dengan beberapa pertanyaan dan jawaban tentang penyakit cabai] -->

---

## ⚠️ Limitasi & Pengembangan Selanjutnya

**Limitasi saat ini:**
- Model dilatih pada dataset terbatas; performa bisa menurun pada kondisi pencahayaan ekstrem
- Chatbot dibatasi pada domain cabai; pertanyaan di luar domain akan memberikan jawaban generik
- Knowledge base bersifat statis; perlu re-ingest jika ada informasi baru

**Rencana pengembangan:**
- [ ] Evaluasi RAG pipeline dengan RAGAS (faithfulness, answer relevancy, context recall)
- [ ] Tambah data augmentasi untuk kondisi lapangan (blur, low-light)
- [ ] Hybrid search (BM25 + semantic) untuk retrieval yang lebih robust
- [ ] Mobile-friendly interface

---

## 👤 Author

**Feri Mauliandi**
Computer Engineering Student — Universitas Syiah Kuala

[![GitHub](https://img.shields.io/badge/GitHub-FeriMauliandi-black?logo=github)](https://github.com/FeriMauliandi)
<!-- [![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/USERNAME_ANDA) -->

---

<div align="center">
<sub>Built as Final Year Project (Tugas Akhir) & AI Engineering Portfolio · 2026</sub>
</div>