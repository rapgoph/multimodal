
import streamlit as st
import numpy as np
import pandas as pd
from fer import FER
from PIL import Image
import cv2




@st.cache
def getEmotions(img):
    detector  = FER(mtcnn=True)
    result = detector.detect_emotions(img)
    data  = result[0]['emotions']
    if data is None:
        st.write('No result')
        return False
    else:
        return data

st.write('This is an app to return emotions of image')

file = st.sidebar.file_uploader('Please upload an image file', type = ['jpg','png'])

if file is None:
    st.write("You haven't uploaded an image file")
else:
    image = Image.open(file)
    img = np.array(image)
    st.image(image, use_column_width=True)
    st.write(pd.DataFrame(getEmotions(img), index=[0]))
