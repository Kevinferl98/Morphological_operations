import numpy as np
import cv2
from PIL import Image
from enum import Enum


class ImageType(Enum):
    BLACK_AND_WHITE = 1
    GREY_SCALE = 2
    COLOR = 3
    UNDEFINED = 4


def dilate(image, structuring_element, is_path, type_of_image):
    if is_path:
        image = cv2.imread(image, 0)

    m, n = structuring_element.shape
    h, w = image.shape
    new_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            top = max(0, i-m//2)
            bottom = min(h, i+m//2+1)
            left = max(0, j-n//2)
            right = min(w, j+n//2+1)
            region = image[top:bottom, left:right]
            k = structuring_element[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
            if type_of_image == ImageType.BLACK_AND_WHITE:
                if np.any((region == 255) & (k == 1)):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = np.max(region[k == 1])
    return new_image


def dilate_color(image, structuring_element, is_path):
    if is_path:
        image = cv2.imread(image, 1)

    m, n = structuring_element.shape
    height, width, channel = image.shape
    new_image = np.zeros((height, width, 3), dtype=np.uint8)
    for ch in range(channel):
        for i in range(height):
            for j in range(width):
                top = max(0, i -m // 2)
                bottom = min(height, i + m // 2 + 1)
                left = max(0, j - n // 2)
                right = min(width, j + n // 2 + 1)
                region = image[top:bottom, left:right, ch]
                k = structuring_element[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                new_image[i][j][ch] = np.max(region[k == 1])
    return new_image


def erode(image, structuring_element, is_path, type_of_image):
    if is_path:
        image = cv2.imread(image, 0)

    m, n = structuring_element.shape
    h, w = image.shape
    new_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            top = max(0, i - m // 2)
            bottom = min(h, i + m // 2 + 1)
            left = max(0, j - n // 2)
            right = min(w, j + n // 2 + 1)
            region = image[top:bottom, left:right]
            k = structuring_element[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
            if type_of_image == ImageType.BLACK_AND_WHITE:
                if np.all(region[k == 1] == 255):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = np.min(region[k == 1])
    return new_image


def erode_color(image, structuring_element, is_path):
    if is_path:
        image = cv2.imread(image, 1)

    m, n = structuring_element.shape
    height, width, channel = image.shape
    new_image = np.zeros((height, width, 3), dtype=np.uint8)
    for ch in range(channel):
        for i in range(height):
            for j in range(width):
                top = max(0, i -m // 2)
                bottom = min(height, i + m // 2 + 1)
                left = max(0, j - n // 2)
                right = min(width, j + n // 2 + 1)
                region = image[top:bottom, left:right, ch]
                k = structuring_element[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                new_image[i][j][ch] = np.min(region[k == 1])
    return new_image


def apertura(image_path, structuring_element, type_of_image):
    image = cv2.imread(image_path, 1 if type_of_image == ImageType.COLOR else 0)
    if type_of_image == ImageType.COLOR:
        return dilate_color(erode_color(image, structuring_element, False), structuring_element, False)
    return dilate(erode(image, structuring_element, False, type_of_image), structuring_element, False, type_of_image)


def chiusura(image_path, structuring_element, type_of_image):
    image = cv2.imread(image_path, 1 if type_of_image == ImageType.COLOR else 0)
    if type_of_image == ImageType.COLOR:
        return erode_color(dilate_color(image, structuring_element, False), structuring_element, False)
    return erode(dilate(image, structuring_element, False, type_of_image), structuring_element, False, type_of_image)


def estrazione_contorni(image_path, structuring_element, type_of_image):
    image = cv2.imread(image_path, 1 if type_of_image == ImageType.COLOR else 0)
    if type_of_image == ImageType.COLOR:
        return dilate_color(image, structuring_element, False) - erode_color(image, structuring_element, False)
    return dilate(image, structuring_element, False, type_of_image) - erode(image, structuring_element, False, type_of_image)


def top_hat(image_path, structuring_element, type_of_image):
    image = cv2.imread(image_path, 1 if type_of_image == ImageType.COLOR else 0)
    return image - apertura(image_path, structuring_element, type_of_image)


def bottom_hat(image_path, structuring_element, type_of_image):
    image = cv2.imread(image_path, 1 if type_of_image == ImageType.COLOR else 0)
    return chiusura(image_path, structuring_element, type_of_image) - image


def classify_image(image_path):
    with Image.open(image_path) as img:
        pixels = list(img.getdata())

        if img.mode == 'L':
            return ImageType.BLACK_AND_WHITE if all(pixel in (0, 255) for pixel in pixels) else ImageType.GREY_SCALE

        is_greyscale = all(pixel[0] == pixel[1] == pixel[2] for pixel in pixels)

        if img.mode == 'RGB':
            return ImageType.GREY_SCALE if is_greyscale else ImageType.COLOR
        if img.mode == 'RGBA':
            all_pixels_are_black_and_white = all(pixel[:3] == (0, 0, 0) or pixel[:3] == (255, 255, 255) for pixel in pixels)
            if all_pixels_are_black_and_white:
                return ImageType.BLACK_AND_WHITE
            return ImageType.GREY_SCALE if is_greyscale else ImageType.COLOR
        return ImageType.UNDEFINED


def is_color_or_undefined(type_of_image) :
    if type_of_image == ImageType.UNDEFINED:
        return True
    return False


structuring_element = np.ones((3, 3), np.uint8)
str2 = np.array([
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
], dtype=np.uint8)
input_path = "lena_bw.png"