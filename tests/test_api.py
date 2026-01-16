import io
import numpy as np
import cv2
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    return app.test_client()

def generate_image():
    img = np.zeros((50, 50), dtype=np.uint8)
    _, buffer = cv2.imencode(".png", img)
    return io.BytesIO(buffer.tobytes())

def test_process_image_ok(client):
    data = {
        "image": (generate_image(), "test.png"),
        "operation": "dilate",
        "shape": "rect",
        "sizeX": "3",
        "sizeY": "3"
    }
    response = client.post("/process_image", data=data, content_type="multipart/form-data")
    assert response.status_code == 200
    assert "image_data" in response.json

def test_process_image_no_file(client):
    response = client.post("/process_image", data={})
    assert response.status_code == 400
