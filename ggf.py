import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage import io

def apply_canny(image):
    # Canny edge detection
    edges = cv2.Canny(image, 100, 200)
    return edges

def apply_preitt(image):
    # Prewitt edge detection
    prewitt_edges = filters.prewitt(image)
    return prewitt_edges

def apply_sobel(image):
    # Sobel edge detection
    sobel_edges = filters.sobel(image)
    return sobel_edges

def apply_roberts(image):
    # Roberts edge detection
    roberts_edges = filters.roberts(image)
    return roberts_edges

def main():
    st.title('Edge Detection on Images')

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        # Read and display image
        image = io.imread(uploaded_file)
        grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Apply edge detection
        st.subheader("Edge Detection Results")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.image(apply_canny(grayscale_image), caption='Canny Edge Detection', use_column_width=True)

        with col2:
            st.image(apply_preitt(grayscale_image), caption='Prewitt Edge Detection', use_column_width=True)

        with col3:
            st.image(apply_sobel(grayscale_image), caption='Sobel Edge Detection', use_column_width=True)

        with col4:
            st.image(apply_roberts(grayscale_image), caption='Roberts Edge Detection', use_column_width=True)

if __name__ == '__main__':
    main()
