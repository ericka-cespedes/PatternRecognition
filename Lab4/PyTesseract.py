import cv2
import sys
import math
import numpy as np
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from tkinter import *
import pytesseract
import os, os.path

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

    specimens = ['a', 'e', 'i', 'o', 'u']
    dirpath = 'Especimenes\\'

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

    porc = [porc_a, porc_e, porc_i, porc_o, porc_u]
    tot = [tot_a, tot_e, tot_i, tot_o, tot_u]

    i=0
    
    for specimen in specimens:
        srcpath = os.path.join(dirpath, specimen)
        print(srcpath)

        for image in os.listdir(srcpath):
            newpath = os.path.join(srcpath, image)
            print(newpath)
            img = cv2.imread(newpath, cv2.IMREAD_GRAYSCALE)
            _,img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
            letter = pytesseract.image_to_string(img)

            tot[i] += 1

            #print(letter[0])
            #print(letter[0] == specimen)

            if letter[0] == specimen:
                porc[i] += 1
                #print(proc[i])

        i += 1

    print("Porcentaje a correctas: ", porc[0]/tot[0]*100)
    print("Porcentaje e correctas: ", porc[1]/tot[1]*100)
    print("Porcentaje i correctas: ", porc[2]/tot[2]*100)
    print("Porcentaje o correctas: ", porc[3]/tot[3]*100)
    print("Porcentaje u correctas: ", porc[4]/tot[4]*100)   
                

##    img = cv2.imread('pytesseract computer.png')
##    if img is None:
##        showinfo(title = 'Error', message = 'No se pudo leer la imagen')
##        sys.exit('No se pudo leer la imagen.')
##
##    print(pytesseract.image_to_string(img))
##    
##    h, w, c = img.shape
##    boxes = pytesseract.image_to_boxes(img) 
##    for b in boxes.splitlines():
##        b = b.split(' ')
##        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
##        
##
##    cv2.imshow('img', img)
##    cv2.imwrite('pytesseract.png', img)

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

