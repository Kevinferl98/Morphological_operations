import numpy as np
import pytest

from app.morphological_operations import (
    dilate, erode, opening, closing,
    top_hat, bottom_hat, contour_extraction,
    ImageType, create_structuring_element
)

@pytest.fixture
def kernel():
    return create_structuring_element("rect", (3, 3))

def grayscale_image():
    return np.array([
        [10, 10, 10],
        [10, 50, 10],
        [10, 10, 10]
    ], dtype=np.uint8)

def bw_image():
    return np.array([
        [0, 0, 0],
        [0, 255, 0],
        [0, 0, 0]
    ], dtype=np.uint8)

def color_image():
    return np.array([
        [[10, 0, 0], [10, 0, 0], [10, 0, 0]],
        [[10, 0, 0], [50, 0, 0], [10, 0, 0]],
        [[10, 0, 0], [10, 0, 0], [10, 0, 0]]
    ], dtype=np.uint8)

def test_dilate_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [50, 50, 50],
        [50, 50, 50],
        [50, 50, 50]
    ], dtype=np.uint8)

    out = dilate(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_erode_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [10, 10, 10],
        [10, 10, 10],
        [10, 10, 10]
    ], dtype=np.uint8)

    out = erode(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_opening_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [10, 10, 10],
        [10, 10, 10],
        [10, 10, 10]
    ], dtype=np.uint8)

    out = opening(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_closing_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [50, 50, 50],
        [50, 50, 50],
        [50, 50, 50]
    ], dtype=np.uint8)

    out = closing(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_top_hat_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [0, 0, 0],
        [0, 40, 0],
        [0, 0, 0]
    ], dtype=np.uint8)

    out = top_hat(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_bottom_hat_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [40, 40, 40],
        [40, 0, 40],
        [40, 40, 40]
    ], dtype=np.uint8)

    out = bottom_hat(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_contour_extraction_greyscale(kernel):
    img = grayscale_image()
    expected = np.array([
        [40, 40, 40],
        [40, 40, 40],
        [40, 40, 40]
    ], dtype=np.uint8)

    out = contour_extraction(img, kernel, ImageType.GREY_SCALE)
    assert np.array_equal(out, expected)

def test_dilate_bw(kernel):
    img = bw_image()
    expected = np.array([
        [255, 255, 255],
        [255, 255, 255],
        [255, 255, 255]
    ], dtype=np.uint8)
    out = dilate(img, kernel, ImageType.BLACK_AND_WHITE)
    assert np.array_equal(out, expected)

def test_erode_bw(kernel):
    img = bw_image()
    expected = np.array([
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ], dtype=np.uint8)
    out = erode(img, kernel, ImageType.BLACK_AND_WHITE)
    assert np.array_equal(out, expected)

def test_dilate_color(kernel):
    img = color_image()
    expected = np.array([
        [[50,0,0],[50,0,0],[50,0,0]],
        [[50,0,0],[50,0,0],[50,0,0]],
        [[50,0,0],[50,0,0],[50,0,0]]
    ], dtype=np.uint8)
    out = dilate(img, kernel, ImageType.COLOR)
    assert np.array_equal(out, expected)

def test_erode_color(kernel):
    img = color_image()
    expected = np.array([
        [[10,0,0],[10,0,0],[10,0,0]],
        [[10,0,0],[10,0,0],[10,0,0]],
        [[10,0,0],[10,0,0],[10,0,0]]
    ], dtype=np.uint8)
    out = erode(img, kernel, ImageType.COLOR)
    assert np.array_equal(out, expected)
