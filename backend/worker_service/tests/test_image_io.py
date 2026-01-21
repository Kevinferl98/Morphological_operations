import pytest
import numpy as np
import io
import base64
from PIL import Image
from worker.utils.image_io import encode_image, load_image_from_bytes

class TestImageIO:

    def test_encode_image_grayscale(self):
        img_array = np.zeros((10, 10), dtype=np.uint8)
        encoded = encode_image(img_array)
        
        assert isinstance(encoded, str)
        decoded_bytes = base64.b64decode(encoded)
        assert decoded_bytes.startswith(b'\x89PNG')

    def test_encode_image_rgb(self):
        img_array = np.zeros((10, 10, 3), dtype=np.uint8)
        encoded = encode_image(img_array)
        
        assert isinstance(encoded, str)
        decoded_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(decoded_bytes))
        assert img.mode == 'RGB'

    def test_load_image_from_bytes_color(self):
        img = Image.new('RGB', (10, 10), color=(255, 0, 0))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()

        loaded_img = load_image_from_bytes(img_bytes)
        
        assert isinstance(loaded_img, np.ndarray)
        assert loaded_img.shape == (10, 10, 3)
        assert np.array_equal(loaded_img[0, 0], [0, 0, 255]) 

    def test_load_image_from_bytes_grayscale_detection(self):
        img = Image.new('RGB', (10, 10), color=(128, 128, 128))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        
        loaded_img = load_image_from_bytes(img_byte_arr.getvalue())
        
        assert len(loaded_img.shape) == 2
        assert loaded_img[0, 0] == 128

    def test_load_image_invalid_bytes(self):
        invalid_bytes = b"not an image"
        with pytest.raises(ValueError, match="Invalid image file"):
            load_image_from_bytes(invalid_bytes)