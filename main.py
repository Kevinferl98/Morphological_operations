import math

import numpy as np
import cv2
import matplotlib.pyplot as plt


def dilate_bw(image, kernel, is_path, is_bw):
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
            if is_bw:
                k = kernel[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                if np.any((region == 255) & (k == 1)):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = region.max()
    return new_image


def erosion_bw(image, kernel, is_path, is_bw):
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
            if is_bw:
                k = kernel[m // 2 - (i - top):m // 2 + (bottom - i), n // 2 - (j - left):n // 2 + (right - j)]
                if np.all((region == 255) & (k == 1)):
                    new_image[i][j] = 255
            else:
                new_image[i][j] = region.min()
    return new_image


def apertura(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return dilate_bw(erosion_bw(image, kernel, False, is_bw), kernel, False, is_bw)


def chiusura(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return erosion_bw(dilate_bw(image, kernel, False, is_bw), kernel, False, is_bw)


def estrazione_contorni(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return dilate_bw(image, kernel, False, is_bw) - erosion_bw(image, kernel, False, is_bw)


def laplaciano(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return dilate_bw(image, kernel, False, is_bw) - erosion_bw(image, kernel, False, is_bw) - 2*image


def top_hat(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return image - apertura(image_path, kernel, is_bw)


def bottom_hat(image_path, kernel, is_bw):
    image = cv2.imread(image_path, 0)
    return chiusura(image_path, kernel, is_bw) - image


kernel = np.ones((3, 3), np.uint8)

input_path = "lena.png"

"""cv2.imwrite("dilate_bw.png", dilate_bw(input_path, kernel, True))
cv2.imwrite("erosion_bw.png", erosion_bw(input_path, kernel, True))
cv2.imwrite("apertura_bw.png", apertura(input_path, kernel))
cv2.imwrite("chiusura_bw.png", chiusura(input_path, kernel))
cv2.imwrite("estrazione_contorni.png", estrazione_contorni(input_path, kernel))
cv2.imwrite("laplaciano.png", laplaciano(input_path, kernel))
cv2.imwrite("top_hat.png", top_hat(input_path, kernel))
cv2.imwrite("bottom_hat.png", bottom_hat(input_path, kernel))"""


myMap = {}
myMap["dilatazione"] = dilate_bw(input_path, kernel, True, True)
myMap["erosione"] = erosion_bw(input_path, kernel, True, True)
myMap["apertura"] = apertura(input_path, kernel, True)
myMap["chiusura"] = chiusura(input_path, kernel, True)
myMap["estrazione_contorni"] = estrazione_contorni(input_path, kernel, True)
myMap["laplaciano"] = laplaciano(input_path, kernel, True)
myMap["top_hat"] = top_hat(input_path, kernel, True)
myMap["bottom_hat"] = bottom_hat(input_path, kernel, True)

num_images = len(myMap)
num_cols = 3
num_rows = math.ceil(num_images/num_cols)

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