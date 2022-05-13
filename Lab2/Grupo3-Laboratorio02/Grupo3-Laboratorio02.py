import cv2
import sys
import numpy as np

def has_inverse_map(a, b, c, d):
    if (b*c-a*d) == 0: 
        return False
    else:
        return True


def w_plane_representation(img, a, b, c, d, titulo):
    height = img.shape[0]
    width = img.shape[1]
    w_plane = np.zeros((height,width,3), np.uint8)
    for i in range(height):
        for j in range(width):
            z = complex(j, i)
            w = (a*z + b) / (c*z + d)
            if w.imag < height and w.real < width:        
                w_plane[int(w.imag), int(w.real)] = img[i, j]
    
    cv2.imshow(titulo, w_plane)
    cv2.imwrite(titulo+'.jpeg', w_plane)
  
  

def lineal_mapping_demonstration(img, a, b, titulo):
    c = 0
    d = 1
    w_plane_representation(img, a, b, c, d, titulo)


def main():
    print('Ingrese el nombre del archivo completo con la extension. EJ: prueba.jpeg')
    fileName = str(input())
    print('Nombre del arhivo: ' + fileName)
    imgR = cv2.imread(fileName)  
    if imgR is None:
        sys.exit("No se pudo leer la imagen.")
        
    a = complex(2.1, 2.1)
    b = 0
    c = complex(0.003, 0)
    d = complex(1, 1)
    w_plane_representation(imgR, a, b, c, d, "Ejercicio 3")
    a = 2
    b = 0
    lineal_mapping_demonstration(imgR, a, b, "Ejercicio 4a")
    a = 3 + 2j
    b = 0
    lineal_mapping_demonstration(imgR, a, b, "Ejercicio 4b")
    a = 1
    b = 10 + 10j
    lineal_mapping_demonstration(imgR, a, b, "Ejercicio 4c")
    a = 3 + 2j
    b = 50 + 50j
    lineal_mapping_demonstration(imgR, a, b, "Ejercicio 4d")


main()
