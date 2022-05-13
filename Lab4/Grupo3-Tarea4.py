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
import shutil, random, os, os.path

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
  print(med_var)
  #mostrar_histograma(med_var[:,0], "Vocal")
  img_hist = get_histogramas(img)
  porc_corr = 0
  for i in range(len(img_hist)):
    #Evalua si el valor del histograma está en el rango de la vocal
    #Si sí está en dicho rango, aumenta 1 fila correcta    
    if img_hist[i] >= med_var[i][0] - math.sqrt(med_var[i][1]) and img_hist[i] <= med_var[i][0] + math.sqrt(med_var[i][1]):
      porc_corr += 1
  
  #Ver cuantas filas son correctas del total y pasar a porcentaje
  porc_corr /= len(img_hist)
  porc_corr *= 100

  return porc_corr

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

def identificador_todas(img):

  print(get_histogramas(img))
  #mostrar_histograma(get_histogramas(img), "a de Danny")
  mod_a = read_model_doc("a")
  mod_e = read_model_doc("e")
  mod_i = read_model_doc("i")
  mod_o = read_model_doc("o")
  mod_u = read_model_doc("u")

  all_porc = []

  print("a")
  porc_a = identificador(img, mod_a)
  all_porc.append(porc_a)
  print("e")
  porc_e = identificador(img, mod_e)
  all_porc.append(porc_e)
  print("i")
  porc_i = identificador(img, mod_i)
  all_porc.append(porc_i)
  print("o")
  porc_o = identificador(img, mod_o)
  all_porc.append(porc_o)
  print("u")
  porc_u = identificador(img, mod_u)
  all_porc.append(porc_u)
  print(all_porc)

  vocal = ""
    
  if all_porc.index(max(all_porc)) == 0:
    vocal = "a"
  if all_porc.index(max(all_porc)) == 1:
    vocal = "e"
  if all_porc.index(max(all_porc)) == 2:
    vocal = "i"
  if all_porc.index(max(all_porc)) == 3:
    vocal = "o"
  if all_porc.index(max(all_porc)) == 4:
    vocal = "u"
    
  return vocal

def main():
    specimens = ['a', 'e', 'i', 'o', 'u']
    images = [' Danny', ' Dario', ' Edwin', ' Ericka', ' Esteban', ' Gerald', ' Nelson', ' Sebastian']

    img = cv2.imread('Cropped\\a Danny0.png')
    if img is None:
        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
        sys.exit('No se pudo leer la imagen.')

    dirpath = 'Especimenes\\'

    thirperc_hu = [""]

    #Se crea un array que tenga todos los histogramas
    hist = get_histogramas(img)
    #Thresholding
    for specimen in specimens:
      srcpath = os.path.join(dirpath, specimen)
      print(srcpath)
      n = len([name for name in os.listdir(srcpath) if os.path.isfile(os.path.join(srcpath, name))])
      setenta = int(n*0.7)

      all_hist = np.zeros((setenta, len(hist), 1), float)

      filenames = random.sample(os.listdir(srcpath), setenta)
      for fname in filenames:
          newpath = os.path.join(srcpath, fname)
          destDirectory = dirpath + specimen + '70\\'
          shutil.move(newpath, destDirectory)
      
      i=0
      print('70')
      for image in os.listdir(destDirectory):
          newpath = os.path.join(destDirectory, image)
          #print(newpath)
          img = cv2.imread(newpath, cv2.IMREAD_GRAYSCALE)
          _,img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
          hist = get_histogramas(img)
          all_hist[i] = hist
          i+=1

      print('30')
      for image in os.listdir(srcpath):
          #print(srcpath)
          newpath = os.path.join(srcpath, image)
          #print(newpath)
          restDirectory = dirpath + specimen + '30\\'
          #print(restDirectory)
          shutil.move(newpath, restDirectory)

      for image in os.listdir(restDirectory):
          #print(restDirectory)
          newpath = os.path.join(restDirectory, image)
          #print(newpath)
          thirperc_hu.append(newpath)


      mod_est = get_sta_mod(all_hist)

      write_model_doc(mod_est, specimen)
      write_model_doc(thirperc_hu, "30")

    print("La letra es una ", identificador_todas(img))

def main2():
    hist_30 = read_model_doc("30")
    porc_a = 0.0
    tot_a = 0
    porc_e = 0.0
    tot_e = 0
    porc_i = 0.0
    tot_i = 0
    porc_o = 0.0
    tot_o = 0
    porc_u = 0.0
    tot_u = 0
    for image in hist_30:
      img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
      if img is not None:
        print("Imagen: ", image[16:])
        vocal_identif = identificador_todas(img)
        print("La letra es una:", vocal_identif, "\n")
        if(image[16] == "a"):
            tot_a += 1
            for i in range(len(vocal_identif)):
                if(image[16] == vocal_identif[i]):
                    porc_a += 1
        if(image[16] == "e"):
            tot_e += 1
            for i in range(len(vocal_identif)):
                if(image[16] == vocal_identif[i]):
                    porc_e += 1
        if(image[16] == "i"):
            tot_i += 1
            for i in range(len(vocal_identif)):
                if(image[16] == vocal_identif[i]):
                    porc_i += 1
        if(image[16] == "o"):
            tot_o += 1
            for i in range(len(vocal_identif)):
                if(image[16] == vocal_identif[i]):
                    porc_o += 1
        if(image[16] == "u"):
            tot_u += 1
            for i in range(len(vocal_identif)):
                if(image[16] == vocal_identif[i]):
                    porc_u += 1
                    
    print("Porcentaje a correctas: ", porc_a/tot_a*100)
    print("Porcentaje e correctas: ", porc_e/tot_e*100)
    print("Porcentaje i correctas: ", porc_i/tot_i*100)
    print("Porcentaje o correctas: ", porc_o/tot_o*100)
    print("Porcentaje u correctas: ", porc_u/tot_u*100)    
