import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *


def preprocessing(img):    
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
    i = minH = minW = maxH = maxW = 0
    lastY = lastX = lastW = lastH = -1

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > 24 and w > 19:                    

            if maxH < h:
                maxH = h

            if maxW < w:
                maxW = w


    maxH +=1
    maxW +=1
    
    # Loop a los bordes
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > 24 and w > 19:

            # Crop
            rect = cv2.rectangle(imgCopy, (x, y), (x + maxW, y + maxH), (0, 0, 0), 0)
             
            # Crop
            cropped = imgCopy[y + int(h/2) - int((maxH/2)):y + int(h/2) + int((maxH/2)), x + int(w/2) - int(maxW/2):x + int(w/2) + int((maxW/2))]
            print("y: ", y, " x: ", x, "\ny+maxH: ", y+maxH, " x+maxW", x+maxW)
            print("N y: ", y-int(((maxH-h)/2)), " N x: ", x-(int((maxW-w)/2)), "\nN y+maxH: ", y + h + int(((maxH-h)/2))), " N x+maxW", x + w + int(((maxW-w)/2))
            
            #print(""+str(h)+", "+str(w)+"")
            cv2.imwrite('Cropped\\cropped'+str(i)+'.png', cropped)

            #if maxH < h:
            #    maxH = h


            #if maxW < w:
            #    maxW = w
            
            
            i+=1

    print('h: ', maxH)
    print('w: ', maxW)

def processImg(fileName):
    img = cv2.imread('Especimenes\\'+fileName, cv2.IMREAD_GRAYSCALE)
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    print(fileName)
    preprocessing(img)

def main():
    specimens = ['a', 'e', 'i', 'o', 'u']
    images = [' Danny.jpg', ' Dario.png', ' Edwin.png', ' Ericka.png', ' Esteban.png', ' Gerald.png', ' Nelson.jpg', ' Sebastian.jpg']
    minHs = [47, 27, 0, 32, 24]
    minWs = [19, 19, 0, 19, 19]

    i = 0
    for specimen in specimens:
        if specimen == 'o':
            for image in images:
                if image == ' Sebastian.jpg':
                    processImg(specimen+image)
        i+=1
