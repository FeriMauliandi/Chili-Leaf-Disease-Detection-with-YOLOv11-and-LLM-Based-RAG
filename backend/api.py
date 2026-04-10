from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import uvicorn
from chains.rag import generate_narrative

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

    # Validasi file gambar
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File yang diunggah harus berupa gambar.")

    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        
        results = model(image)
        
        detected_labels = {}
        
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            label = model.names[cls_id]

            if label not in detected_labels or confidence > detected_labels[label]:
                detected_labels[label] = confidence

        # Susun respons JSON dan panggil RAG
        detections = []
        for label, confidence in detected_labels.items():
            label_capitalized = label.capitalize()
            
            # Panggil fungsi RAG untuk mendapatkan penjelasan
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
            "results": detections
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan saat memproses gambar: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)