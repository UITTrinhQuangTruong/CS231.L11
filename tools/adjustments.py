import numpy as np
import math


def brightness_contrast(img_a, brightness=255, contrast=127):
    brightness /= 255
    contrast /= 255
    k = math.tan((45 + 44 * contrast)/180 * np.pi)

    output = (img_a-127.5*(1-brightness))*k + 127.5*(1+brightness)
    output[output > 255] = 255
    output[output < 0] = 0
    return output.astype(np.uint8)
