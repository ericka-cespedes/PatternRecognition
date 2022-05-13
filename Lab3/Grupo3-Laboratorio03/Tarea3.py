#Código obtenido de https://learnopencv.com/edge-detection-using-opencv/
import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *


def main():
    filetypes = (
        ('jpeg files', ('*.jpeg', '*.jpg')),
        ('png files', '*.png'),
        ('All files', '*.*')
    )
    
    root = Tk()
    fileName = fd.askopenfilename(initialdir = '/', title = 'Seleccione la imagen', filetypes = filetypes)
    showinfo(title = 'Archivo seleccionado', message = fileName)
    
    # Read the original image
    img = cv2.imread(fileName)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    # Display original image
    cv2.imshow('Original', img)

    # Convert to graycsale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image for better edge detection
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 

    # Sobel Edge Detection
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3) # Sobel Edge Detection on the X axis
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3) # Sobel Edge Detection on the Y axis
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3) # Combined X and Y Sobel Edge Detection

    laplacian = cv2.Laplacian(img_blur,cv2.CV_64F)

    # Display Sobel Edge Detection Images
    cv2.imshow('Sobel x', sobelx)
    cv2.imwrite('sobelx.jpeg', sobelx)
    cv2.imshow('Sobel y', sobely)
    cv2.imwrite('sobely.jpeg', sobely)
    cv2.imshow('Sobel xy', sobelxy)
    cv2.imwrite('sobelxy.jpeg', sobelxy)
    cv2.imshow('Laplacian', laplacian)
    cv2.imwrite('laplacian.jpeg', laplacian)

    # Canny Edge Detection
    edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
    # Display Canny Edge Detection Image
    cv2.imshow('Canny', edges)
    cv2.imwrite('canny.jpeg', edges)
