# Gunakan versi Python yang stabil untuk library AI
FROM python:3.10-slim

# Bikin user non-root sesuai aturan Hugging Face (Wajib)
RUN useradd -m -u 1000 user
USER user

# Set environment variables agar perintah Python terbaca
ENV PATH="/home/user/.local/bin:$PATH"

# Set folder kerja di dalam container
WORKDIR /app

# Salin file requirements terlebih dahulu untuk caching yang efisien
COPY --chown=user ./requirements.txt requirements.txt

# Install dependencies (tambahkan library sistem tambahan jika YOLO membutuhkannya)
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Salin SELURUH file proyek Anda (termasuk folder chroma_data dan model YOLO)
COPY --chown=user . /app

# Jalankan FastAPI di port 7860 (Wajib)
# PENTING: Jika file utama FastAPI Anda bernama api.py, ubah "app:app" menjadi "api:app"
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "7860"]