import cv2
import numpy as np
#  import matplotlib.pyplot as plt


def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, 100, 255)
    # return the edged image
    return edged


def BGRA(img, back_eraser=False, mode='canny', opacity=1):
    d = img.shape[-1]
    if d <= 3:
        output = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        if back_eraser:
            if mode == 'canny':
                canny = auto_canny(img)
                #  plt.imshow(canny)
                #  plt.show()
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
                closing = closing.astype(np.uint8) * 255
                contour, hier = cv2.findContours(closing, cv2.RETR_CCOMP,
                                                 cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contour:
                    cv2.drawContours(closing, [cnt], 0, 255, -1)
                mask = (closing > 0)
            output[:, :, 3] = mask.astype(np.uint8) * 255
            #  plt.imshow(output[:, :, 3])
            #  plt.show()
            if mode == '':
                pass
    else:
        output = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
 
    return fill(output, opacity=opacity)


def fill(img, opacity):
    output = img.copy()
    output[:, :, 3] = (opacity * output[:, :, 3]).astype(np.uint8)
    return output


def BGRAtoGRAYA(img):
    output = cv2.cvtColor(img[:, :, :3], cv2.COLOR_RGB2GRAY)

    return output, img[:, :, 3]


def GRAYA2BGRA(img, mask):
    output = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    output[:, :, 3] = mask

    return output


def graymask(img):
    output, mask = BGRAtoGRAYA(img)
    return GRAYA2BGRA(output, mask)


def RGBA(img, back_eraser=False, mode='canny', opacity=1):
    d = img.shape[-1]
    if d <= 3:
        output = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
        if back_eraser:
            if mode == 'canny':
                canny = cv2.Canny(img, 50, 150)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                closing = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel)
                closing = closing.astype(np.uint8) * 255
                contour, hier = cv2.findContours(closing, cv2.RETR_CCOMP,
                                                 cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contour:
                    cv2.drawContours(closing, [cnt], 0, 255, -1)
                mask = (closing > 0)
            output[:, :, 3] = mask
            if mode == '':
                pass
    else:
        output = img.copy()

    return fill(output, opacity=opacity)
