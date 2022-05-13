import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\erick\AppData\Local\Programs\Tesseract-OCR\tesseract'

def preprocessing(img, minH, minW, error):    
    # OTSU threshold
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    #cv2.imshow('thresh1', thresh1)
    cv2.imwrite('tresh1.png', thresh1)

    #Si hay puntos afuera
    # 3 erosion, 3 dilatacion

    #Si no letras con puntos dentro -> dilatacion
    #Si no hay puntos afuera entonces aplico dilatacion erosion
    
    # Estructura y tamanho de kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Dilatacion
    dilation = cv2.dilate(thresh1, kernel, iterations = 3)
    #cv2.imshow('dilation', dilation)
    cv2.imwrite('dilation.png', dilation)

    # Erosion
    erosion = cv2.erode(dilation, kernel, iterations = 3)  
    #cv2.imshow('erode', erosion)
    cv2.imwrite('erode.png', erosion)

    # Bordes
    contours, hierarchy = cv2.findContours(erosion, cv2.RETR_EXTERNAL,
                                                     cv2.CHAIN_APPROX_NONE)
    # Copia de la imagen final
    imgCopy = erosion.copy()
    i = maxH = maxW = 0
     
    # Loop a los bordes
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > minH and w > minW:

            if maxH < h:
                maxH = h

            if maxW < w:
                maxW = w
            
    maxH +=1
    maxW +=1
    
    # Cortar y centrar
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > minH and w > minW and i != error:

            cropped = imgCopy[y:y + h, x:x + w]

            new_image = np.zeros((maxH,maxW),np.uint8)

            #Getting the centering position
            ax,ay = (maxW - w)//2,(maxH - h)//2

            #Pasting the 'image' in a centering position
            new_image[ay:h+ay,ax:ax+w] = cropped
            
            cv2.imwrite('Cropped\\cropped'+str(i)+'.png', new_image)
            print('Cropped\\cropped'+str(i)+'.png')
            
            i+=1

def processImg(fileName, minH, minW, error):
    img = cv2.imread('Especimenes\\'+fileName, cv2.IMREAD_GRAYSCALE)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    print(fileName)
    preprocessing(img, minH, minW, error)

def main():
    specimens = ['a', 'e', 'o', 'u']
    images = [' Danny.jpg', ' Dario.png', ' Edwin.png', ' Ericka.png', ' Esteban.png', ' Gerald.png', ' Nelson.jpg', ' Sebastian.jpg']
    minHs = [69, 27, 58, 29, 32, 27, 30, 37]
    minWs = [64, 19, 55, 27, 24, 43, 75, 29]

    for specimen in specimens:
        i=0
        for image in images:
            if specimen == 'e' and image == ' Nelson.jpg':
                #Hay una en error en esta en especifico
                processImg(specimen+image, minHs[i], minWs[i], 11)
                i+=1
            else:
                processImg(specimen+image, minHs[i], minWs[i], -1)
                i+=1
