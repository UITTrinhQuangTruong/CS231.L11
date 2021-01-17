import cv2
import numpy as np
#  import matplotlib.pyplot as plt


def alpha(img_a, img_b, al=1):
    """
        Blending anh theo cong thuc:
            I = (1 - Alpha)*Img + Alpha*channel

        Ap dung vao truong hop ghep anh effect vao anh goc
        Para:
            img: Anh goc
            channel: Anh effect
            mask: Mask de ap dung effect
            alpha: Mac dinh 0.3
    """
    out = img_a.copy()
    out = (out * al + img_b * (1 - al)).astype(np.uint8)

    return out


def normal(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
    Che do blend don gian, cong thuc la:
        f(a, b) = b
    """

    output = img_a.copy()
    if resize:
        h, w = img_a.shape[:2]
        img_b = cv2.resize(img_b, (w, h))
        alpha = (img_b[:, :, 3])
        back = 255 - alpha
        alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGRA).astype(np.float) / 255
        back = cv2.cvtColor(back, cv2.COLOR_GRAY2BGRA).astype(np.float) / 255

        output = np.zeros_like(img_a)
        output = alpha * img_b + back * img_a
        output[output > 255] = 255
    else:
        h, w = img_b.shape[:2]
        output[x:h + x, y:w + y] = normal(img_a[x:h + x, y:w + y],
                                          img_b,
                                          resize=True)
    output[:, :, 3] = (opacity * img_a[:, :, 3])
    #  plt.imshow(cv2.cvtColor(img_b, cv2.COLOR_BGRA2RGBA))
    #  plt.show()
    return output.astype(np.uint8)


def dissolve(img_a, img_b, resize=True, opacity=0.5, x=0, y=0):
    """
    Lay ngau nhien cac pixel roi blend, tao hieu ung nhieu pixel!!!
    Ngau nhien lay diem tren a va b
    """

    if resize:
        # Lay hinh dang cua anh
        h, w = img_a.shape[:2]
        img_b = cv2.resize(img_b, (w, h))
        size = h * w
        num_ones = int(opacity * size)

        # tao mat na ngau nhien
        mask = np.zeros((size)).astype(np.bool)
        mask[:num_ones] = True
        np.random.shuffle(mask)
        mask = mask.reshape((h, w))

        output = img_a.copy()
        output[mask] = img_b[mask]
    else:
        ha, wa, daa = img_a.shape[:2]
        output = np.zeros((ha + hb * 2, wa + wb, daa))
        output[hb:hb + ha, wb] = 0
        output[x:h + x, y:h + y] = dissolve(img_a[x:shape_b[0] + x,
                                                  y:shape_b[1] + y],
                                            img_b,
                                            resize=True)

    # output[:, :, 3] = (opacity*output[:, :, 3]).astype(np.uint8)
    return output


def dark(out, a, b, alpha_a, alpha_b):
    mask = a > b
    out[mask] = (b[mask] * alpha_b[mask] + a[mask] *
                 (255 - alpha_b[mask])) / 255
    out[~mask] = (a[~mask] * alpha_a[~mask] + b[~mask] *
                  (255 - alpha_a[~mask])) / 255
    return out


def darken(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
    Blend giu lai cac pixel co gia tri nho hon cua anh
    """

    if resize:
        h, w = img_a.shape[:2]
        rimg_b = cv2.resize(img_b, (w, h)).astype(np.float)
        rimg_a = img_a.astype(np.float)
        alpha_a = rimg_a[:, :, 3]
        blue_a, green_a, red_a = rimg_a[:, :, 0], rimg_a[:, :, 1], rimg_a[:, :,
                                                                          2]

        alpha_b = rimg_b[:, :, 3]
        blue_b, green_b, red_b = rimg_b[:, :, 0], rimg_b[:, :, 1], rimg_b[:, :,
                                                                          2]

        output = np.zeros_like(img_a)
        mask_alpha = alpha_a > alpha_b

        output[:, :, 0] = dark(output[:, :, 0], blue_a, blue_b, alpha_a,
                               alpha_b)

        output[:, :, 1] = dark(output[:, :, 1], green_a, green_b, alpha_a,
                               alpha_b)

        output[:, :, 2] = dark(output[:, :, 2], red_a, red_b, alpha_a, alpha_b)
        output[:, :, 3] = alpha_a

        output[:, :, 3] = (opacity * output[:, :, 3]).astype(np.uint8)
        return output.astype(np.uint8)


def multiply(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
    Blend 2 anh bang phep nhan ma tran

    f(a, b) = a * b
    """
    if resize:
        h, w = img_a.shape[:2]
        img_b = cv2.resize(img_b, (w, h)).astype(np.uint8)
        output = np.zeros_like(img_a).astype(np.float)

        a = img_a[:, :, :3].astype(np.float)
        b = img_b[:, :, :3].astype(np.float)
        alpha_a = img_a[:, :, 3].astype(np.float)
        # cv2.cvtColor(
        #     img_a[:, :, 3], cv2.COLOR_GRAY2BGR).astype(np.float)
        alpha_b = img_b[:, :, 3].astype(np.float)

        # Nhan alpha voi 3 kenh mau cua anh
        a_3d = np.stack([alpha_a] * 3, axis=2)
        b_3d = np.stack([alpha_b] * 3, axis=2)
        output[:, :, :3] = (a*b*b_3d/255 + (255-b_3d) * a) / \
            255   # Cong them pixel nen
        output[:, :, 3] = alpha_a*(255-alpha_b) / \
            255 + alpha_b*alpha_a / 255 + alpha_b*(255 - alpha_a)/255
        # print(output[:, :, 3])
        output[output > 255] = 255

    output[:, :, 3] = (opacity * output[:, :, 3]).astype(np.uint8)
    return np.ceil(output).astype(np.uint8)


def screen(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
    Blend anh theo cong thuc:
        f(a, b) = 1 - (1 - a)(1 - b)
    """

    if resize:
        h, w = img_a.shape[:2]
        img_b = (cv2.resize(img_b, (w, h))).astype(np.uint8)

        alpha_b = img_b[:, :, 3]
        output = ((1 - (1 - img_a / 255.0) * (1 - img_b / 255.0)) * 255)

        output[output > 255] = 255
        output = output.astype(np.uint8)

    output[:, :, 3] = (opacity * output[:, :, 3]).astype(np.uint8)
    return output


def overlay(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
    Blend anh theo cong thuc:
        + 2ab, if a < 0.5
        + 1 - 2(1 - a)(1 - b), otherwise
    """

    if resize:
        h, w = img_a.shape[:2]
        img_b = (cv2.resize(img_b, (w, h))).astype(np.uint8)

        a = img_a.astype(float) / 255
        b = img_b.astype(float) / 255  # make float on range 0-1

        mask = (a >= 0.5)  # generate boolean mask of everywhere a > 0.5
        # generate an output container for the blended image
        ab = np.zeros_like(a)

        # now do the blending
        ab[~mask] = (2 * a * b)[~mask]  # 2ab everywhere a<0.5
        ab[mask] = (1 - 2 * (1 - a) * (1 - b))[mask]  # else this
        ab = (ab * 255).astype(np.uint8)

        ab[:, :, 3] = (opacity * ab[:, :, 3]).astype(np.uint8)
        return ab


def softlight(img_a, img_b, resize=True, opacity=1, x=0, y=0):
    """
        App dung cong thuc cua Photoshop 2012:
        + 2ab + a^2(1 - 2b), if b < 0.5
        + 2a(1 - b) +sqrt(a)(2b - 1), otherwise
    """

    if resize:
        h, w = img_a.shape[:2]
        img_b = (cv2.resize(img_b, (w, h))).astype(np.uint8)

        a = img_a.astype(np.float) / 255
        b = img_b.astype(np.float) / 255

        mask = (b >= 0.5)

        ab = np.zeros_like(a)

        ab[~mask] = (2 * (a * b) + (a**2) * (1 - 2 * b))[~mask]
        ab[mask] = ((2 * a) * (1 - b) + np.sqrt(a) * (2 * b - 1))[mask]
        ab = (ab * 255).astype(np.uint8)

        ab[:, :, 3] = (opacity * ab[:, :, 3]).astype(np.uint8)
        return ab



def test(img_a, img_b):
    out = darken(img_a, img_b)
    #  plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGRA2RGBA))
    #  plt.show()
