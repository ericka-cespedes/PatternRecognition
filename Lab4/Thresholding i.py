import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
#import pytesseract

#pytesseract.pytesseract.tesseract_cmd = r'C:\Users\erick\AppData\Local\Programs\Tesseract-OCR\tesseract'

def preprocessing(img, minH, minW, nombre, error):    
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
    i = 0
            
    size = height = width = 166
    
    # Cortar y centrar
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > minH and w > minW and i != error:

            cropped = imgCopy[y:y + h, x:x + w]
            #cv2.imwrite('Cropped\\'+nombre+str(i)+'cropped.png', cropped)

            new_image = np.zeros((size,size),np.uint8)

            dim = (width, height)
 
            # resize image
            resized = cv2.resize(cropped, dim, interpolation = cv2.INTER_AREA)
            #cv2.imwrite('Cropped\\'+nombre+str(i)+'resized.png', resized)
            
            #Getting the centering position
            ax,ay = (size - width)//2,(size - height)//2

            #Pasting the 'image' in a centering position
            new_image[ay:height+ay,ax:ax+width] = resized
            
            cv2.imwrite('Cropped\\'+nombre+str(i)+'.png', new_image)
            #print('Cropped\\'+nombre+str(i)+'.png')
            
            i+=1

def processImg(fileName, minH, minW, error):
    img = cv2.imread('Especimenes\\'+fileName, cv2.IMREAD_GRAYSCALE)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    print(fileName[:-4])
    print(minH)
    print(minW)
    preprocessing(img, minH, minW, fileName[:-4], error)

def main():
    specimens = ['a', 'e', 'i', 'o', 'u']
    images = [' Danny.jpg', ' Dario.png', ' Edwin.png', ' Ericka.png', ' Esteban.png', ' Gerald.png', ' Nelson.jpg', ' Sebastian.jpg']
    minHs = [69, 13, 23, 20, 20, 27, 73, 37]
    minWs = [42, 0, 0, 0, 0, 0, 0, 0]

    for specimen in specimens:
        i = 0
        if specimen == 'i':
            for image in images:
                if image == ' Nelson.jpg':
                    processImg(specimen+image, minHs[i], minWs[i], -1)
                i+=1
