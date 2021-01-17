import cv2
import numpy as np
#  import matplotlib.pyplot as plt
#
#  from cvt import BGRA


def stylization(img, sigma_s, sigma_r):
    output = img.copy()
    output[:, :, :3] = cv2.stylization(output[:, :, :3],
                                       sigma_s=sigma_s,
                                       sigma_r=sigma_r)

    return output


def oilPaint(img):
    output = img.copy()
    output[:, :, :3] = cv2.xphoto.oilPainting(output[:, :, :3], 7, 1)
    return output


def detailEnhan(img, sigma_s, sigma_r):
    return cv2.detailEnhance(src=img, sigma_s=sigma_s, sigma_r=sigma_r)


def invert(img):
    output = np.zeros_like(img)
    output[:, :, :3] = cv2.bitwise_not(img[:, :, :3])
    output[:, :, 3] = img[:, :, 3]

    return output


def gamma_function(channel, gamma):
    invGamma = 1 / gamma
    table = np.array([((i / 255.0)**invGamma) * 255 for i in np.arange(0, 256)
                      ]).astype("uint8")  # creating lookup table
    channel = cv2.LUT(channel, table)
    return channel


def summer(img, blue_ratio=0.75, red_ratio=1.25, sat_ratio=1.2):
    output = img.copy()

    output[:, :, 2] = gamma_function(img[:, :, 2], blue_ratio)

    output[:, :, 0] = gamma_function(img[:, :, 0], red_ratio)

    hsv = cv2.cvtColor(output[:, :, :3], cv2.COLOR_RGB2HSV)
    hsv[:, :, 1] = gamma_function(hsv[:, :, 1], sat_ratio)
    output[:, :, :3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return output


def l60tvs(img, thresh):
    output = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

    h, w = img.shape[:2]

    size = h * w
    num_ones = int(thresh * size)

    # tao mat na ngau nhien
    mask = np.zeros((size)).astype(np.bool)
    mask[:num_ones] = True
    np.random.shuffle(mask)
    mask = mask.reshape((h, w))

    output[~mask] = np.random.randint(0, 255, size=(h, w))[~mask]

    return output


def pencil_sk(img, kernel_size=25):
    gray = cv2.cvtColor(img, cv2.COLOR_RGBA2GRAY)

    # Blur the image using Gaussian Blur
    gray_blur = cv2.GaussianBlur(gray, (kernel_size, kernel_size), 0)

    # Convert the image into pencil sketch
    output = cv2.divide(gray, gray_blur, scale=250.0)

    return output


def mask_hsv(hsv, l, u):
    if l > u:
        return mask_hsv(hsv, l, 180) + mask_hsv(hsv, 0, u)
    lower = np.array([l, 100, 100])  # setting lower HSV value
    upper = np.array([u, 255, 255])  # setting upper HSV value
    mask = cv2.inRange(hsv, lower, upper) > 0  # generating mask
    return mask


def splash(img, l, u):
    img_a = img[:, :, :3]

    hsv = cv2.cvtColor(img_a, cv2.COLOR_RGB2HSV)
    res = np.zeros_like(img_a)
    mask = mask_hsv(hsv, l, u)

    gray = cv2.cvtColor(cv2.cvtColor(img_a, cv2.COLOR_RGB2GRAY),
                        cv2.COLOR_GRAY2BGR)

    res[~mask] = gray[~mask]
    res[mask] = img_a[mask]

    return res


def pencil(img, sigma_s, sigma_r, shade_factor, color=True):
    dst_gray, dst_color = cv2.pencilSketch(img,
                                           sigma_s=sigma_s,
                                           sigma_r=sigma_r,
                                           shade_factor=shade_factor)
    if color:
        return dst_color
    return dst_gray


#  img = cv2.imread('../test/fire.jpg', -1)
#
#  img = BGRA(img)
#
#  out = splash(img, 160, 30)
#
#  plt.imshow(out)
#  plt.show()
