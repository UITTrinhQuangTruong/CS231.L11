# pyright: reportGeneralTypeIssues=false
# pyright: reportMissingImports=false

import cv2
from tools import blending as bm
from tools.cvt import BGRA, graymask
from tools.adjustments import brightness_contrast
from tools.layereffect import lmask
from tools.filter import *
import streamlit as st
#import matplotlib.pyplot as plt
# cv2.imshow("Goc", img)


def retro(img, theta=0.02, alpha=0.3, channel=0):
    """
        Ap dung hieu ung 3D retro vao anh
        Para:
            img: input image
            theta: Do day duong retro
            alpha: do dam nhat cua anh
            beta: do dam nhat cua effect
    """
    # Tinh do dam cua duong
    length = int(theta*img.shape[1])
    out = img.copy()

    out[:, :-length, channel] = bm.alpha(out[:, : -length, channel],
                                   out[:, length:, channel], alpha)
    return out


def art1(img, back=2, opacity=0.5, type_effect=1):

    background = BGRA('art/back/back%d.png' % back, False)

    b1 = graymask(img)

    p1 = BGRA('art/art1/p1.png', False, opacity=opacity)
    b2 = bm.multiply(b1, p1)

    b3 = bm.normal(background, b2)
    return b3


def art2(img, back=1, opacity=1, type_effect=2):
    background = BGRA('art/back/back%d.png' % back, False)

    b1 = graymask(img)

    p1 = BGRA('art/art1/p1.png', False, opacity=opacity)
    b2 = lmask(b1, p1, type_effect)
    b3 = bm.normal(background, b2)

    p2 = BGRA('art/art1/p2.png', False)
    b4 = bm.normal(b3, p2)
    return b4


def art3(img, back=1, brightness=-33, contrast1=50, contrast2=30):
    background = BGRA('art/back/back%d.png' % back, False)

    b1 = graymask(img)
    b2 = bm.normal(background, b1)

    brightness = st.sidebar.slider('Brightness', -255, 255, 0, 1)
    contrast1 = st.sidebar.slider('Contrast 1', -127, 127, 0, 1)
    b2[:, :, :3] = brightness_contrast(
        b2[:, :, :3], brightness=brightness, contrast=contrast1)

    p1 = BGRA('art/art3/p1.png', False)
    b3 = bm.softlight(b2, p1)

    p2 = BGRA('art/art3/p2.png', False)
    b4 = bm.overlay(b3, p2)

    contrast2 = st.sidebar.slider('Contrast 2', -127, 127, 0, 1)
    b4[:, :, :3] = brightness_contrast(b4[:, :, :3], 0, contrast=contrast2)
    p3 = BGRA('art/art3/p3.png', False)
    b5 = lmask(b4, p3, 2)
    p4 = BGRA('art/art3/p4.png')
    b6 = bm.overlay(b5, p4)
    p5 = BGRA('art/art3/p5.png')
    b7 = bm.normal(b6, p5)
    p6 = BGRA('art/art3/p6.png')
    return bm.softlight(b7, p6)

    return b2


def art4(img):
    background = BGRA('art/back/back2.png')

    grayimg = graymask(img)
    grayimg[:, :, :3] = cv2.stylization(
        grayimg[:, :, :3], sigma_s=60, sigma_r=0.6)
    return bm.normal(background, grayimg)


def Blending(img_a, img_b, mode='Normal', resize=True, x=0, y=0):
    if mode == 'Normal':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 1.0, 0.01)
        return bm.normal(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Dissolve':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)
        return bm.dissolve(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Darken':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)

        return bm.darken(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Multiply':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)

        return bm.multiply(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Screen':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)

        return bm.screen(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Overlay':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)

        return bm.overlay(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)

    if mode == 'Softlight':
        opacity = st.sidebar.slider(
            'Tăng giảm opacity (càng giảm ảnh nằm trên càng nhat)', 0.0, 1.0, 0.5, 0.01)

        return bm.softlight(img_a, img_b, resize=resize, opacity=opacity, x=x, y=y)


def Art(img, mode='Art 1', opacity=1, brightness=-33, contrast1=50, contrast2=30):
    if mode == 'Art 1':
        return art1(img, opacity=opacity)
    if mode == 'Art 2':
        return art2(img=img,  opacity=opacity)
    if mode == 'Art 3':
        return art3(img,  brightness=brightness, contrast1=contrast1, contrast2=contrast2)
    if mode == 'Art 4':
        return art4(img)
    if mode == 'Retro':
        channel = st.sidebar.selectbox('Channel:', ('R', 'G', 'B'))
        r = st.sidebar.slider('Do lech:' ,0.0, 1.0, 0.02, 0.01)
        if channel == 'B': 
            return retro(img,theta=r, channel=2)
        if channel == 'G':
            return retro(img, theta=r, channel=1)
        return retro(img, theta=r)


def Filters(img, mode='Detail Enhancement'):
#      if mode == 'Detail Enhancement':
    #      sigma_s = st.sidebar.slider('Sigmal s', 1, 50, 10, 1)
    #      sigma_r = st.sidebar.slider('Sigmal r', 0.15, 1.0, 0.15, 0.15)
    #      return detailEnhan(img, sigma_s, sigma_r)
    #
    #  if mode == 'Invert':
    #      return invert(img)
    #
    #  if mode == 'Summer':
    #      blue_ratio = st.sidebar.slider('Blue gamma', 0.25, 1.0, 0.75, 0.05)
    #      red_ratio = st.sidebar.slider('Red gamma', 1.0, 2.0, 1.25, 0.05)
    #      sat_ratio = st.sidebar.slider('Saturation gamma', 1.0, 2.0, 1.2, 0.1)
    #      return summer(img, blue_ratio=blue_ratio, red_ratio=red_ratio, sat_ratio=sat_ratio)
    #  if mode == 'Winter':
    #      blue_ratio = st.sidebar.slider('Blue gamma', 1.0, 2.0, 1.25, 0.05)
    #      red_ratio = st.sidebar.slider('Red gamma', 0.1, 1.0, 0.75, 0.05)
    #      sat_ratio = st.sidebar.slider('Saturation gamma', 0.1, 1.0, 0.8, 0.1)
    #      return summer(img, blue_ratio=blue_ratio, red_ratio=red_ratio, sat_ratio=sat_ratio)
    #  if mode == '60TVs':
    #      thresh = st.sidebar.slider('Thresh', 0.0, 1.0, 0.8, 0.01)
    #      return l60tvs(img, thresh)
    #  if mode == 'Sepia':
    #      return sepia(img)
    #
    #  if mode == 'Pencil Sketch':
    #      kernel_size = 25
 #         return pencil_sk(img, kernel_size=kernel_size)
    if mode == 'Splash':
        l = st.sidebar.slider('Chọn ngưỡng dưới', 0, 180, 15, 1)
        u = st.sidebar.slider('Chọn ngưỡng trên', 0, 180, 30, 1)
        return splash(img, l, u)

    
    #  if mode == 'Pencil':
    #      color = st.sidebar.checkbox('Ảnh màu', True)
    #      sigma_s = st.sidebar.slider('Sigmal s', 1, 200, 60, 1)
    #      sigma_r = st.sidebar.slider('Sigmal r', 0.0, 1.0, 0.07, 0.01)
    #      shade_factor = st.sidebar.slider('Shade factor', 0.0, 0.1, 0.05, 0.01)
    #      output = img.copy()
    #      if color:
    #          output[:, :, :3] = pencil(
    #              output[:, :, :3], sigma_s, sigma_r, shade_factor, color)
    #      else:
    #          output = pencil(
    #              output[:, :, :3], sigma_s, sigma_r, shade_factor, color)
    #
    #      return output
    #  if mode == 'Oil Painting Effect':
    #      return oilPaint(img)
    #
    #  if mode == 'Water color Effect':
    #      sigma_s = st.sidebar.slider('Sigmal s', 1, 200, 60, 1)
    #      sigma_r = st.sidebar.slider('Sigmal r', 0.0, 1.0, 0.07, 0.01)
    #
     #     return stylization(img, sigma_s, sigma_r)
    if mode == 'Retro':
        channel = st.sidebar.selectbox('Channel:', ('R', 'G', 'B'))
        r = st.sidebar.slider('Do lech:' ,0.0, 1.0, 0.02, 0.01)
        if channel == 'B': 
            return retro(img,theta=r, channel=2)
        if channel == 'G':
            return retro(img, theta=r, channel=1)
        return retro(img, theta=r)


"""
Kiem thu
"""


"""image = Image.open('test/cauvang.png')

img_a = np.array(image)

out = art1(img_a)
plt.imshow(out)
plt.show()"""
