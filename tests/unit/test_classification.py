import numpy as np
from app.morphological_operations import classify_image_array, ImageType

def test_binary_image():
    img = np.array([[0, 255], [255, 0]], dtype=np.uint8)
    assert classify_image_array(img) == ImageType.BLACK_AND_WHITE

def test_grayscale_image_2d():
    img = np.array([[10, 20], [30, 40]], dtype=np.uint8)
    assert classify_image_array(img) == ImageType.GREY_SCALE

def test_grayscale_image_3d():
    gray = np.array([[50, 80], [90, 120]], dtype=np.uint8)
    img = np.stack([gray, gray, gray], axis=-1)
    assert classify_image_array(img) == ImageType.GREY_SCALE

def test_color_image():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[..., 0] = 255
    assert classify_image_array(img) == ImageType.COLOR