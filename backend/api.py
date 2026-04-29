from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import uvicorn
import base64 
import cv2 
import numpy as np 
from pydantic import BaseModel
from src.chains.rag import generate_narrative
from src.chains.chain import create_rag_chain

app = FastAPI(
    title="ChiliCare API",
    description="API Pendeteksi Penyakit Daun Cabai dengan YOLOv11 dan LLM RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = YOLO("model/bestv11.pt")
except Exception as e:
    print(f"Error memuat model YOLO: {e}")
    model = None

@app.get("/")
def read_root():
    return {"message": "Selamat datang di ChiliCare API. Gunakan endpoint /detect untuk inferensi."}

@app.post("/detect")
async def detect_disease(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model YOLO belum siap atau tidak ditemukan.")

    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        results = model(image)
        
        # --- MULAI KODE BARU UNTUK GAMBAR ---
        # 1. Ambil gambar hasil deteksi (berupa array BGR)
        annotated_frame = results[0].plot()
        # 2. Ubah BGR ke RGB
        rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        # 3. Ubah menjadi objek PIL Image
        img_pil = Image.fromarray(rgb_image)
        # 4. Simpan ke buffer dan konversi ke Base64
        buffered = io.BytesIO()
        img_pil.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        # --- AKHIR KODE BARU UNTUK GAMBAR ---

        detected_labels = {}
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls_id]

            if label not in detected_labels or confidence > detected_labels[label]:
                detected_labels[label] = confidence

        detections = []
        for label, confidence in detected_labels.items():
            label_capitalized = label.capitalize()
            narrative = generate_narrative(label_capitalized)
            
            detections.append({
                "class": label_capitalized,
                "confidence": round(confidence, 2),
                "narrative": narrative
            })

        return {
            "status": "success",
            "filename": file.filename,
            "total_detections": len(detections),
            "results": detections,
            "image_base64": img_base64 # Tambahkan gambar base64 ke respons
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")
    
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_expert(request: QuestionRequest):
    try:
        # Panggil RAG text chain
        rag_chain = create_rag_chain()
        
        # Jalankan RAG (LangChain otomatis akan mencari konteks dan memanggil LLM)
        jawaban = rag_chain.invoke(request.question)
        
        return {
            "status": "success",
            "question": request.question,
            # Output dari StrOutputParser() di chain.py sudah langsung berupa string jawaban
            "answer": jawaban 
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan pada LLM: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)