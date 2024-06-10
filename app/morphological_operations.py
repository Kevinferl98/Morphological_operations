import numpy as np
import cv2
from PIL import Image
from enum import Enum


class ImageType(Enum):
    BLACK_AND_WHITE = 1
    GREY_SCALE = 2
    COLOR = 3
    UNDEFINED = 4


class StructuringElementType(Enum):
    RECT = 'rect'
    ELLIPSE = 'ellipse'
    CROSS = 'cross'


class OperationType(Enum):
    DILATE = 'dilate'
    ERODE = 'erode'
    APERTURA = 'opening'
    CHIUSURA = 'closing'
    CONTORNI = 'contorni'
    TOP_HAT = 'top_hat'
    BOTTOM_HAT = 'bottom_hat'


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


def is_undefined(type_of_image) :
    if type_of_image == ImageType.UNDEFINED:
        return True
    return False


def create_structuring_element(structuring_element_type, size):
    if structuring_element_type == StructuringElementType.RECT.value:
        return cv2.getStructuringElement(cv2.MORPH_RECT, size)
    elif structuring_element_type == StructuringElementType.ELLIPSE.value:
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, size)
    elif structuring_element_type == StructuringElementType.CROSS.value:
        return cv2.getStructuringElement(cv2.MORPH_CROSS, size)
    else:
        return ValueError('Forma non valida')


def execute_operation(operation_type, structuring_element, file_path, image_type):
    if operation_type == OperationType.DILATE.value:
        if image_type == ImageType.COLOR:
            res = dilate_color(file_path, structuring_element, True)
        else:
            res = dilate(file_path, structuring_element, True, image_type)
    elif operation_type == OperationType.ERODE.value:
        if image_type == ImageType.COLOR:
            res = erode_color(file_path, structuring_element, True)
        else:
            res = erode(file_path, structuring_element, True, image_type)
    elif operation_type == OperationType.APERTURA.value:
        res = apertura(file_path, structuring_element, image_type)
    elif operation_type == OperationType.CHIUSURA.value:
        res = chiusura(file_path, structuring_element, image_type)
    elif operation_type == OperationType.CONTORNI.value:
        res = estrazione_contorni(file_path, structuring_element, image_type)
    elif operation_type == OperationType.TOP_HAT.value:
        res = top_hat(file_path, structuring_element, image_type)
    elif operation_type == OperationType.BOTTOM_HAT.value:
        res = bottom_hat(file_path, structuring_element, image_type)
    
    if image_type == ImageType.COLOR:
        return convert_bgr_to_rgb(res)
    return res
    

def convert_bgr_to_rgb(bgr_image):
    rgb_image = np.zeros_like(bgr_image)
    rgb_image[:, :, 0] = bgr_image[:, :, 2]
    rgb_image[:, :, 1] = bgr_image[:, :, 1]
    rgb_image[:, :, 2] = bgr_image[:, :, 0]

    return rgb_image