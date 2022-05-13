import cv2
import numpy as np
import sys
from tkinter import filedialog
from tkinter.messagebox import showinfo
from tkinter import ttk
from tkinter import *

def xDerivative(img, w, h):
    imgX = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            if x+1 >= w:
                imgX[x, y] = int(img[x-1, y]) - int(img[x,y])

            else:
                imgX[x, y] = int(img[x+1, y]) - int(img[x,y])

    return imgX


def yDerivative(img, w, h):
    imgY = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            if y+1 >= h:
                imgY[x, y] = int(img[x, y-1]) - int(img[x,y])

            else:
                imgY[x, y] = int(img[x, y+1]) - int(img[x,y])

    return imgY

def supDerivatives(img, imgX, imgY, w, h):
    imgRes = np.zeros([w,h,1], np.uint8)
    for x in range(w):
        for y in range(h):
            supX = imgX[x,y]/2
            supY = imgY[x,y]/2
            imgRes[x, y] = int(supX + supY)

    return imgRes

def select_file():
    filetypes = (
        ('jpeg files', ('*.jpeg','*.jpg')),
        ('png files', '*.png')
        ('All files', '*.*')
    )

    fileName = fd.askopenfilename(
        title='Seleccione un archivo',
        initialdir='/',
        filetypes=filetypes)

    showinfo(
        title='Archivo seleccionado:',
        message=fileName
    )

def main():
##    print('Ingrese el nombre del archivo completo con la extension. EJ: prueba.jpeg')
##    fileName = str(input())
##    print('Nombre del arhivo: ' + fileName)
##    img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)

    root = Tk()
    root.title('Laboratorio 03')

    # open button
    open_button = ttk.Button(
        root,
        text='Abrir un archivo',
        command=select_file
    )

    open_button.pack(expand=True)

    img = cv2.imread(fileName, cv2.IMREAD_GRAYSCALE)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit("No se pudo leer la imagen.")

    (w, h) = img.shape[:2]

    imgResX = xDerivative(img, w, h)
    cv2.imwrite('imgResX.jpeg', imgResX)
    cv2.imshow('imgResX', imgResX)
    
    imgResY = yDerivative(img, w, h)
    cv2.imwrite('imgResY.jpeg', imgResY)
    cv2.imshow('imgResY', imgResY)

    imgRes = supDerivatives(img, imgResX, imgResY, w, h)
    cv2.imwrite('imgRes.jpeg', imgRes)
    cv2.imshow('imgRes', imgRes)
