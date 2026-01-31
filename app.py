import streamlit as st
from PIL import Image
from ultralytics import YOLO
import cv2
import torch
import tempfile
import os
from chains.rag import generate_narrative


st.set_page_config(page_title="ourchamplie", layout="centered")
st.title("🌿Aplikasi Pendeteksi Penyakit Daun Cabai")


@st.cache_resource
def load_model():
    model = YOLO("model/best.pt") 
    return model

model = load_model()
uploaded_file = st.file_uploader("Unggah gambar daun cabai anda", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Gambar yang Diupload", use_container_width=True)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        image.save(temp_file.name)
        temp_path = temp_file.name

    st.info("🔍 Mendeteksi daun...")

    results = model(temp_path)
    annotated_frame = results[0].plot()
    rgb_image = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
    st.image(rgb_image, caption="Hasil Deteksi Penyakit", use_container_width=True)

    st.subheader("📋 Hasil Deteksi:")

    detected_labels = {}

    for box in results[0].boxes:
        cls_id = int(box.cls[0])
        confidence = float(box.conf[0])
        label = model.names[cls_id]

        if label not in detected_labels or confidence > detected_labels[label]:
            detected_labels[label] = confidence

    for label, confidence in detected_labels.items():
        st.markdown(f"### 🌱 {label.capitalize()} (skor: {confidence:.2f})")
    

  
        with st.spinner("📖 Menyusun penjelasan..."):
            narrative = generate_narrative(label.capitalize())

        st.subheader("🧠 Penjelasan")
        st.write(narrative)



    os.remove(temp_path)
