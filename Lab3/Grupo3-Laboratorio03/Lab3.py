import cv2
import numpy as np
import sys
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *

def xDerivative(img, w, h):
    imgX = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            if x+1 >= w:
                imgX[x, y] = abs(int(img[x-1, y]) - int(img[x,y]))

            else:
                imgX[x, y] = abs(int(img[x+1, y]) - int(img[x,y]))

    return imgX


def yDerivative(img, w, h):
    imgY = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            if y+1 >= h:
                imgY[x, y] = abs(int(img[x, y-1]) - int(img[x,y]))

            else:
                imgY[x, y] = abs(int(img[x, y+1]) - int(img[x,y]))

    return imgY

def sumDerivatives(img, imgX, imgY, w, h):
    imgRes = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            supX = imgX[x,y]/2
            supY = imgY[x,y]/2
            imgRes[x, y] = int(supX + supY)

    return imgRes

def main():

    filetypes = (
        ('jpeg files', ('*.jpeg', '*.jpg')),
        ('png files', '*.png'),
        ('All files', '*.*')
    )
    
    root = Tk()
    fileName = fd.askopenfilename(initialdir = '/', title = 'Seleccione la imagen', filetypes = filetypes)
    showinfo(title = 'Archivo seleccionado', message = fileName)
    img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    (w, h) = img.shape[:2]

    imgResX = xDerivative(img, w, h)
    cv2.imwrite('imgResX.jpeg', imgResX)
    cv2.imshow('imgResX', imgResX)
    
    imgResY = yDerivative(img, w, h)
    cv2.imwrite('imgResY.jpeg', imgResY)
    cv2.imshow('imgResY', imgResY)

    imgRes = sumDerivatives(img, imgResX, imgResY, w, h)
    cv2.imwrite('imgRes.jpeg', imgRes)
    cv2.imshow('imgRes', imgRes)
