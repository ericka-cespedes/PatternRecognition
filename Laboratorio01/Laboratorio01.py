import cv2
import sys

def lab1():

    print('Ingrese el nombre del archivo completo con la extension. EJ: prueba.jpeg')
    fileName = str(input())
    print('Nombre del arhivo: ' + fileName)

    img = cv2.imread(fileName)

    if img is None:
        sys.exit("No se pudo leer la imagen.")

    rows = img.shape[0]
    cols = img.shape[1]
    for i in range(rows):
        for j in range(cols):
            if( (i%2 == 0 and j%2 == 0) or (i%2 != 0 and j%2 !=0) ):
                img[i, j] = [0, 0, 0]

    cv2.imshow('Imagen modificada con pixeles negros',img)
    #Guardar imagen con pix negros
    cv2.imwrite('imagenPixNegros.jpeg', img)

    for i in range(rows):
        for j in range(cols):
            if( (i%2 == 0 and j%2 == 0) or (i%2 != 0 and j%2 !=0) ):
                img[i, j] = [255, 255, 255]
                
    cv2.imshow('Imagen modificada con pixeles blancos',img)
    cv2.imwrite('imagenPixBlancos.jpeg', img)
