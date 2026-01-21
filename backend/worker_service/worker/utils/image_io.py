import numpy as np
from PIL import Image
import base64
import io
import cv2

def encode_image(image: np.ndarray) -> str:
    if len(image.shape) == 2:
        pil_img = Image.fromarray(image.astype('uint8'), 'L')
    else:
        pil_img = Image.fromarray(image.astype('uint8'), 'RGB')

    buffer = io.BytesIO()
    pil_img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def load_image_from_bytes(file_bytes):
    array = np.frombuffer(file_bytes, np.uint8)
    image = cv2.imdecode(array, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Invalid image file")
    
    if image.ndim == 3:
        if np.all(image[..., 0] == image[..., 1]) and np.all(image[..., 1] == image[..., 2]):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return image