import cv2
import numpy as np


def lmask(img, mask, resize=True, type_effect=1):
    a = img[:, :, :3]
    mask_a = img[:, :, 3]
    a[mask_a == 0] = 0
    if resize:
        mask = cv2.resize(mask, (a.shape[1], a.shape[0]))
        b = mask[:, :, :3] * 1.0 / 255
        mask_b = mask[:, :, 3]

        a = (a * b).astype(np.uint8)
        output = cv2.cvtColor(a, cv2.COLOR_BGR2BGRA)
        if type_effect == 1:
            output[:, :, 3] = mask_b
        elif type_effect == 2:
            mask_b = ((mask_b / 255) * mask_a).astype(np.uint8)
            output[:, :, 3] = mask_b
        return output
