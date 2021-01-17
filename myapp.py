import streamlit as st
import numpy as np
from PIL import Image
from tools import cvt
from process import Blending, Filters

###############################################################################

st.write('''
          # "Photoshop hóa" ảnh dễ dàng!


          ''')

st.write("### Một ứng dụng nhỏ nhỏ trong một thế giới to to")

mode_image = st.sidebar.selectbox('Bạn muốn sử dụng cái gì?',
                                  ('Blending Image', 'Filter Image'))

if mode_image is None:
    st.text("Chọn một chế độ để biến ảnh thành nghệ thuật thôi!!!")
else:
    if mode_image == 'Blending Image':
        file_a = st.sidebar.file_uploader("Upload ảnh 1", type=["jpg", "png"])
        back_eraser_a = st.sidebar.checkbox("Delete background", key=0)
        file_b = st.sidebar.file_uploader("Upload ảnh 2", type=["jpg", "png"])
        back_eraser_b = st.sidebar.checkbox("Delete background", key=1)

        if file_a is None or file_b is None:
            st.warning('Hãy Upload đủ ảnh yêu cầu!')
        else:
            image_a = Image.open(file_a)
            img_a = cvt.RGBA(np.array(image_a), back_eraser=back_eraser_a)

            image_b = Image.open(file_b, )
            img_b = cvt.RGBA(np.array(image_b), back_eraser=back_eraser_b)
            Resize = st.sidebar.checkbox('Resize ảnh', True)
            option = st.sidebar.selectbox(
                'Bạn chọn chế độ Blending nào?',
                ('Normal', 'Dissolve', 'Darken', 'Multiply', 'Screen',
                 'Overlay', 'Softlight'))
            st.header("Ảnh đầu vào")
            col1, col2 = st.beta_columns(2)
            with col1:
                st.text("Ảnh 1")
                st.image(image_a, use_column_width=True)
            with col2:
                st.text("Ảnh 2")
                st.image(image_b, use_column_width=True)

            st.header("Ảnh đầu ra")
            output = Blending(img_a, img_b, option, resize=Resize)
            st.image(output, use_column_width=True)
    else:
        file_a = st.sidebar.file_uploader("Upload ảnh 1", type=["jpg", "png"])
        back_eraser_a = st.sidebar.checkbox("Delete background", key=0)

        if file_a is None:
            st.warning('Hãy Upload đủ ảnh yêu cầu!')

        else:
            image_a = Image.open(file_a)
            img_a = cvt.RGBA(np.array(image_a), back_eraser=back_eraser_a)

            st.text("Ảnh đầu vào")
            st.image(image_a, use_column_width=True)

            if mode_image == 'Filter Image':
                mode_filter = st.sidebar.selectbox('Chọn Filter áp dụng',
                                                   ('Splash', 'Retro'))
                output = Filters(img_a, mode=mode_filter)
            #  elif mode_image == 'Pro Effect':
            #      mode_effect = st.sidebar.selectbox(
            #          'Chọn hiệu ứng áp dụng',
            #          ('Retro', 'Art 1', 'Art 2', 'Art 3', 'Art 4'))
            #      output = Art(img_a, mode=mode_effect)
            #  else:
            #      brightness = st.sidebar.slider('Brightness', -255, 255, 0, 1)
            #      contrast = st.sidebar.slider('Contrast', -127, 127, 0, 1)
            #
            #      output = brightness_contrast(img_a, brightness, contrast)

            st.header("Ảnh đầu ra")
            st.image(output, use_column_width=True)
