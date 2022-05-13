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

def get_vocal_hu(im):
    # Calculate Moments
    moments = cv2.moments(im)
    # Calculate Hu Moments
    huMoments = cv2.HuMoments(moments)
    for i in range(0,7):
        huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

    return huMoments

def get_sta_mod(hu_list):
  sta_model = np.zeros((len(hu_list[0]), 2), float)
  
  #Loop por cada histograma
  #Para sacar medias
  for i in range(len(hu_list)):
    #Loop por cada línea del histograma
    for j in range(len(hu_list[i])):
      sta_model[j][0] = np.add(sta_model[j][0], hu_list[i][j])      
    
  sta_model[:,0] /= len(hu_list)

  #Loop para sacar varianzas
  for i in range(len(hu_list)):
    for j in range(len(hu_list[i])):
      sub = np.subtract(hu_list[i][j], sta_model[j][0]) ** 2
      sta_model[j][1] = np.add(sta_model[j][1], sub)
  
  #Varianza poblacional es decir /N
  sta_model[:,1] /= len(hu_list)


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
    img_hu = get_vocal_hu(img)
    porc_corr = 0
    
    for i in range(len(img_hu)):
        #Evalua si el valor del histograma está en el rango de la vocal
        #Si sí está en dicho rango, aumenta 1 fila correcta    
        if img_hu[i] >= med_var[i][0] - math.sqrt(med_var[i][1]) and img_hu[i] <= med_var[i][0] + math.sqrt(med_var[i][1]):
          porc_corr += 1
    
    #Ver cuantas filas son correctas del total y pasar a porcentaje
    porc_corr /= len(img_hu)
    porc_corr *= 100

    return porc_corr

def identificador_todas(img):
  #print(get_vocal_hu(img))

  mod_a = read_model_doc("a")
  #print(mod_a)
  mod_e = read_model_doc("e")
  #print(mod_e)
  #mod_i = read_model_doc("i")  
  mod_o = read_model_doc("o")
  #print(mod_o)
  mod_u = read_model_doc("u")
  #print(mod_u)
  all_porc = []

  #print("a")
  porc_a = identificador(img, mod_a)
  all_porc.append(porc_a)
  #print("e")
  porc_e = identificador(img, mod_e)
  all_porc.append(porc_e)
  #porc_i = identificador(img, mod_i)
  #all_porc.append(all_porc, porc_i)
  all_porc.append(0)
  #print("o")
  porc_o = identificador(img, mod_o)
  all_porc.append(porc_o)
  #print("u")
  porc_u = identificador(img, mod_u)
  all_porc.append(porc_u)
  #print(all_porc)

  vocal = ""
  
  if max(all_porc) == all_porc[0]:
    vocal += " a"
  if max(all_porc) == all_porc[1]:
    vocal += " e"
  if max(all_porc) == all_porc[2]:
    vocal += " i"
  if max(all_porc) == all_porc[3]:
    vocal += " o"
  if max(all_porc) == all_porc[4]:
    vocal += " u"
    
  return vocal

def main():
    specimens = ['a', 'e', 'o', 'u']
    images = [' Danny', ' Dario', ' Edwin', ' Ericka', ' Esteban', ' Gerald', ' Nelson', ' Sebastian']

    sevperc_hu = np.zeros((int(((40*8)*70)/100), 7, 1), float)
    thirperc_hu = [""]

    #Recorrer por vocal
    for specimen in specimens:        
        i_sevperc=0
        i_thirperc=0
        #Recorrer por persona
        for image in images:
            #Recorrer los 40 de cada persona
            for i in range(40):
                img = cv2.imread('Cropped\\'+specimen+image+str(i)+'.png', cv2.IMREAD_GRAYSCALE)
                if img is not None:
                    if i_sevperc < int(((40*8)*70)/100):
                        _,img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
                        sevperc_hu[i_sevperc] = get_vocal_hu(img);
                        i_sevperc += 1
                    else:
                        str_temp = 'Cropped\\'+specimen+image+str(i)+'.png'
                        thirperc_hu.append(str_temp)              
                        i_thirperc += 1

        mod_est = get_sta_mod(sevperc_hu)
      
        write_model_doc(mod_est, specimen)
        write_model_doc(thirperc_hu, "30")


        
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
        print("Imagen: ", image[8:])
        vocal_identif = identificador_todas(img)
        print("La letra es una:", vocal_identif, "\n")
        if(image[8] == "a"):
            tot_a += 1
            for i in range(len(vocal_identif)):
                if(image[8] == vocal_identif[i]):
                    porc_a += 1
        if(image[8] == "e"):
            tot_e += 1
            for i in range(len(vocal_identif)):
                if(image[8] == vocal_identif[i]):
                    porc_e += 1
        if(image[8] == "i"):
            tot_i += 1
            for i in range(len(vocal_identif)):
                if(image[8] == vocal_identif[i]):
                    porc_i += 1
        if(image[8] == "o"):
            tot_o += 1
            for i in range(len(vocal_identif)):
                if(image[8] == vocal_identif[i]):
                    porc_o += 1
        if(image[8] == "u"):
            tot_u += 1
            for i in range(len(vocal_identif)):
                if(image[8] == vocal_identif[i]):
                    porc_u += 1
                    
    print("Porcentaje a correctas: ", porc_a/tot_a*100)
    print("Porcentaje e correctas: ", porc_e/tot_e*100)
    #print("Porcentaje i correctas: ", porc_i/tot_i*100)
    print("Porcentaje o correctas: ", porc_o/tot_o*100)
    print("Porcentaje u correctas: ", porc_u/tot_u*100)    
