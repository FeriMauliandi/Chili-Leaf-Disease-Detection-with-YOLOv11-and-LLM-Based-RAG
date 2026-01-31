# Chilicare: Chili Leaf Disease Detection with YOLOv11 and Structured RAG

**Chilicare** adalah sebuah proyek AI untuk mendeteksi penyakit pada daun tanaman cabai menggunakan model deteksi objek **YOLOv11**, lalu memberikan penjelasan hasil deteksi melalui sistem **LLM dengan Structured Retrieval‑Augmented Generation (RAG)**.

---

## Fitur Utama

-  **Deteksi Penyakit Daun Cabai**  
  Menggunakan model deteksi objek **YOLOv11** untuk mengidentifikasi area daun yang terinfeksi.

-  **Interpretasi dengan LLM + Structured RAG**  
  Memanfaatkan model bahasa besar (*LLM*) dengan mekanisme *Structured RAG* untuk memberikan penjelasan terkait hasil deteksi dan rekomendasi lanjutan.

-  **Aplikasi API / Web Antarmuka**  
  Tersedia skrip utama (`app.py`) untuk menjalankan layanan deteksi melalui antarmuka web Streamlit.

-  **Pelatihan Model**  
  Notebook pelatihan (`train_yolo11_chili_leaf_disease_detection.ipynb`) berisi pipeline data, augmentasi, dan pelatihan YOLOv11.

-  **Data JSON**  
  File `data.json` menyimpan referensi data, label, atau konteks yang digunakan dalam RAG.

---
