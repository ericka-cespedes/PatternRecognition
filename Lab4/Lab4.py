import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import math
import matplotlib.pyplot as plt

def get_histogramas(img):
  height = img.shape[0]
  width = img.shape[1]
  
  hist_height = np.zeros((int(height/4)+1, 1), np.uint8)
  hist_width = np.zeros((int(width/4)+1, 1), np.uint8)
  
  n_pixeles_i = 0
  for i in range(height):
    n_pixeles_i += 1
    if n_pixeles_i > 4:
      n_pixeles_i = 0

    n_pixeles_j = 0
    for j in range(width):
      n_pixeles_j += 1
      if n_pixeles_j >= 4:
        n_pixeles_j = 0

      if np.sum(img[i, j]) == 0:
        hist_height[i//4] += 1
        hist_width[j//4] += 1
          
  
  return np.concatenate([hist_height, hist_width])

def mostrar_histograma(histo, nombre):
  x_number_list = histo[0]
  y_number_list = histo[1]

  plt.hist(histo)
  
  
  plt.title(nombre)

  plt.xlabel("Número de pixel")
  plt.ylabel("Valor")
  plt.show()

def preprocessing(img, minH, minW, nombre, error):    
    # OTSU threshold
    ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    #cv2.imshow('thresh1', thresh1)
    #cv2.imwrite('tresh1.png', thresh1)

    #Si hay puntos afuera
    # 3 erosion, 3 dilatacion

    #Si no letras con puntos dentro -> dilatacion
    #Si no hay puntos afuera entonces aplico dilatacion erosion
    
    # Estructura y tamanho de kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Dilatacion
    dilation = cv2.dilate(thresh1, kernel, iterations = 3)
    #cv2.imshow('dilation', dilation)
    #cv2.imwrite('dilation.png', dilation)

    # Erosion
    erosion = cv2.erode(dilation, kernel, iterations = 3)  
    #cv2.imshow('erode', erosion)
    #cv2.imwrite('erode.png', erosion)

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
    preprocessing(img, minH, minW, fileName[:-4], error)

def getHistograma(fileName):
    img = cv2.imread('Cropped\\'+fileName[:-4]+'0.png')
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    print(fileName[:-4]+'0.png')
    hist = get_histogramas(img)
    nombreHist = "Histograma de la primera " + fileName[0] + " de " + fileName[2:-4]
    #Solo mostramos una letra de cada persona, para no mostrar muchos
    mostrar_histograma(hist, nombreHist)

def main():
    specimens = ['a', 'e', 'i', 'o', 'u']
    images = [' Danny.jpg', ' Dario.png', ' Edwin.png', ' Ericka.png', ' Esteban.png', ' Gerald.png', ' Nelson.jpg', ' Sebastian.jpg']
    minHs = [69, 27, 58, 29, 32, 27, 30, 37]
    minWs = [64, 19, 55, 27, 24, 43, 75, 29]

    #Thresholding
    for specimen in specimens:
        i=0
        for image in images:
            if specimen == 'e' and image == ' Nelson.jpg':
                #Hay una en error en esta en especifico
                processImg(specimen+image, minHs[i], minWs[i], 11)
                #getHistograma(specimen+image)
                i+=1
            else:
                processImg(specimen+image, minHs[i], minWs[i], -1)
                #getHistograma(specimen+image)
                i+=1
