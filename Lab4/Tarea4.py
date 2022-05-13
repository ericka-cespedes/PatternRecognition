import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import math
import matplotlib.pyplot as plt
import pickle
import random

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

def get_sta_mod(hist_list):
  #Modelo estad. donde [][0] = promedio y [][1] = varianza
  #Cambié orden de largos
  sta_model = np.zeros((len(hist_list[0]), 2), float)
  
  #Loop por cada histograma
  #Para sacar medias
  for i in range(len(hist_list)):
    #Loop por cada línea del histograma
    for j in range(len(hist_list[i])):
      sta_model[j][0] = np.add(sta_model[j][0], hist_list[i][j])      
    
  sta_model[:,0] /= len(hist_list)

  #Loop para sacar varianzas
  for i in range(len(hist_list)):
    for j in range(len(hist_list[i])):
      sub = np.subtract(hist_list[i][j], sta_model[j][0]) ** 2
      sta_model[j][1] = np.add(sta_model[j][1], sub)
  
  #Varianza poblacional es decir /N
  sta_model[:,1] /= len(hist_list)


  return sta_model

#Escribir un documento .data con las medias y varianzas
def write_model_doc(model, vocal):
  str = 'med_&_var'+vocal+'.data'
  with open(str, 'wb') as filehandle:    
    pickle.dump(model, filehandle)

#Leer un documento .data con las medias y varianzas
def read_model_doc(vocal):
  str = 'med_&_var'+vocal+'.data'
  with open(str, 'rb') as filehandle:
    # read the data as binary data stream
    sta_model = pickle.load(filehandle)
  return sta_model

#Recibe una imagen a evaluar y el histograma con medias y varianzas de cierta vocal
#Identifica si esa imagen es de ese tipo de vocal
def identificador(img, med_var):
  img_hist = get_histogramas(img)
  porc_corr = 0
  for i in range(len(img_hist)):
    #Evalua si el valor del histograma está en el rango de la vocal
    #Si sí está en dicho rango, aumenta 1 fila correcta
    if img_hist[i] >= med_var[i][0] - math.sqrt(med_var[i][1]):
      porc_corr += 1
    elif img_hist[i] <= med_var[i][0] + math.sqrt(med_var[i][1]):
      porc_corr += 1
  
  #Ver cuantas filas son correctas del total y pasar a porcentaje
  porc_corr /= len(img_hist)
  porc_corr *= 100

  return True if porc_corr > 80 else False

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
            
    size = 166
    
    # Cortar y centrar
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        #Los valores minimos de todas las letras para no tire basura
        if h > minH and w > minW and i != error:

            cropped = imgCopy[y:y + h, x:x + w]

            new_image = np.zeros((size,size),np.uint8)

            #Getting the centering position
            ax,ay = (size - w)//2,(size - h)//2

            #Pasting the 'image' in a centering position
            new_image[ay:h+ay,ax:ax+w] = cropped
            
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
    specimens = ['a', 'e', 'o', 'u']
    images = [' Danny', ' Dario', ' Edwin', ' Ericka', ' Esteban', ' Gerald', ' Nelson', ' Sebastian']

    img = cv2.imread('Cropped\\a Danny0.png')
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    #Se crea un array que tenga todos los histogramas
    hist = get_histogramas(img)
    all_hist = np.zeros((40, len(hist), 1), float)
    #Thresholding
    for specimen in specimens:
      i=0
      for image in images:
          img = cv2.imread('Cropped\\'+specimen+image+str(i)+'.png')
          if img is None:
              showinfo(title = 'Error', message = 'No se pudo leer la imagen')
              sys.exit('No se pudo leer la imagen.')

          hist = get_histogramas(img)
          all_hist[i] = hist

          i+=1
      
      #70% de todos los datos
      sev_perc_data = int((len(all_hist)*70)/100)
      #hist_70 = 
      
      #Prueba con un array con 2 histogramas
      #mod_est = get_sta_mod(  [[[100], [200], [300]],[[50],[100],[150]]])
      
      mod_est = get_sta_mod(all_hist)

      write_model_doc(mod_est, specimen)
