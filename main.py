import math

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from enum import Enum


class ImageType(Enum):
    BLACK_AND_WHITE = 1
    GREY_SCALE = 2
    COLOR = 3
    UNDEFINED = 4


def dilate(image, kernel, is_path, type_of_image):
    if is_path:
        image = cv2.imread(image, 0)

    m, n = kernel.shape
    h, w = image.shape
    new_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            top = max(0, i-m//2)
            bottom = min(h, i+m//2+1)
            left = max(0, j-n//2)
            right = min(w, j+n//2+1)
            region = image[top:bottom, left:right]
            if type_of_image == ImageType.BLACK_AND_WHITE:
                k = kernel[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                if np.any((region == 255) & (k == 1)):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = region.max()
    return new_image


def erosion(image, kernel, is_path, type_of_image):
    if is_path:
        image = cv2.imread(image, 0)

    m, n = kernel.shape
    h, w = image.shape
    new_image = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            top = max(0, i - m // 2)
            bottom = min(h, i + m // 2 + 1)
            left = max(0, j - n // 2)
            right = min(w, j + n // 2 + 1)
            region = image[top:bottom, left:right]
            if type_of_image == ImageType.BLACK_AND_WHITE:
                k = kernel[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                if np.all((region == 255) & (k == 1)):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = region.min()
    return new_image


def apertura(image_path, kernel, type_of_image):
    image = cv2.imread(image_path, 0)
    return dilate(erosion(image, kernel, False, type_of_image), kernel, False, type_of_image)


def chiusura(image_path, kernel, type_of_image):
    image = cv2.imread(image_path, 0)
    return erosion(dilate(image, kernel, False, type_of_image), kernel, False, type_of_image)


def estrazione_contorni(image_path, kernel, type_of_image):
    image = cv2.imread(image_path, 0)
    return dilate(image, kernel, False, type_of_image) - erosion(image, kernel, False, type_of_image)


def top_hat(image_path, kernel, type_of_image):
    image = cv2.imread(image_path, 0)
    return image - apertura(image_path, kernel, type_of_image)


def bottom_hat(image_path, kernel, type_of_image):
    image = cv2.imread(image_path, 0)
    return chiusura(image_path, kernel, type_of_image) - image


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
    if type_of_image == ImageType.COLOR or type_of_image == ImageType.UNDEFINED:
        return True
    return False


def execute(input_path, kernel):
    type_of_image = classify_image(input_path)
    if is_color_or_undefined(type_of_image):
        print('Passare un\'immagine in bianco e nero o a scala di grigi')
        return
    print('tipo di immagine: ', type_of_image)
    myMap = {}
    myMap["originale"] = cv2.imread(input_path, 0)
    myMap["dilatazione"] = dilate(input_path, kernel, True, type_of_image)
    myMap["erosione"] = erosion(input_path, kernel, True, type_of_image)
    myMap["apertura"] = apertura(input_path, kernel, type_of_image)
    myMap["chiusura"] = chiusura(input_path, kernel, type_of_image)
    myMap["estrazione_contorni"] = estrazione_contorni(input_path, kernel, type_of_image)
    myMap["top_hat"] = top_hat(input_path, kernel, type_of_image)
    myMap["bottom_hat"] = bottom_hat(input_path, kernel, type_of_image)

    num_images = len(myMap)
    num_cols = 3
    num_rows = math.ceil(num_images / num_cols)

    fig, axs = plt.subplots(num_rows, num_cols, figsize=(8, 8))

    if num_rows == 1:
        axs = axs.reshape(1, -1)
    elif num_cols == 1:
        axs = axs.reshape(-1, 1)

    for ax, (titolo, immagine) in zip(axs.flat, myMap.items()):
        ax.imshow(immagine, cmap='gray')
        ax.set_title(titolo)

    for ax in axs.flat[num_images:]:
        ax.axis('off')

    plt.tight_layout()
    plt.show()


kernel = np.ones((3, 3), np.uint8)
input_path = "lena_bw.png"
execute(input_path, kernel)