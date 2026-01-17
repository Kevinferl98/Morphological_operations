import io
import numpy as np
import cv2

def generate_image(size=(50, 50), value=0):
    img = np.full(size, value, dtype=np.uint8)
    _, buffer = cv2.imencode(".png", img)
    return io.BytesIO(buffer.tobytes())