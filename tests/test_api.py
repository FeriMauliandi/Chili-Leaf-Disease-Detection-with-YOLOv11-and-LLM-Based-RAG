import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
import io
from PIL import Image

from backend.api import app

client = TestClient(app)

def test_read_root():
    """Test root endpoint / returns 200 and expected message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "ChiliCare API" in response.json()["message"]

@patch("backend.api.model")
def test_detect_disease_invalid_file_type(mock_model):
    """Test /detect rejects non-image file uploads with 400 Bad Request."""
    files = {"file": ("test.txt", b"dummy content", "text/plain")}
    response = client.post("/detect", files=files)
    assert response.status_code == 400
    assert "gambar" in response.json()["detail"]

@patch("backend.api.model")
@patch("backend.api.generate_narrative")
def test_detect_disease_success(mock_generate_narrative, mock_model):
    """Test /detect endpoint with a valid image file and mocked YOLO model."""
    mock_generate_narrative.return_value = "Saran penanganan penyakit kuning."
    
    # Mock YOLO model box output
    mock_box = MagicMock()
    mock_box.cls = [0]
    mock_box.conf = [0.95]
    
    mock_result = MagicMock()
    mock_result.boxes = [mock_box]
    # plot() returns a dummy numpy array representing RGB image
    import numpy as np
    mock_result.plot.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
    
    mock_model.return_value = [mock_result]
    mock_model.names = {0: "kuning"}
    
    # Create a small dummy image in bytes
    img = Image.new("RGB", (50, 50), color="green")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    img_bytes = img_byte_arr.getvalue()
    
    files = {"file": ("chili_leaf.jpg", img_bytes, "image/jpeg")}
    response = client.post("/detect", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["total_detections"] == 1
    assert data["results"][0]["class"] == "Kuning"
    assert data["results"][0]["narrative"] == "Saran penanganan penyakit kuning."

@patch("backend.api.create_rag_chain")
def test_ask_expert_endpoint(mock_create_rag_chain):
    """Test /ask endpoint streaming response from RAG chain."""
    mock_chain = MagicMock()
    mock_chain.stream.return_value = ["Tanaman ", "cabai ", "membutuhkan ", "air."]
    mock_create_rag_chain.return_value = mock_chain
    
    payload = {"question": "Bagaimana penyiraman cabai?"}
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 200
    assert "Tanaman cabai membutuhkan air." in response.text
