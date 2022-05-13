import cv2 as cv
import math
import numpy as np

# Procesamiento en escala de grises
def rgb2gray(img):
    h=img.shape[0]
    w=img.shape[1]
    img1=np.zeros((h,w),np.uint8)
    for i in range(h):
        for j in range(w):
            img1[i,j]=0.144*img[i,j,0]+0.587*img[i,j,1]+0.299*img[i,j,1]
    return img1

 # Calcular el núcleo de convolución gaussiano
def gausskernel(size):
    sigma=1.0
    gausskernel=np.zeros((size,size),np.float32)
    for i in range (size):
        for j in range (size):
            norm=math.pow(i-1,2)+pow(j-1,2)
            gausskernel [i, j] = math.exp (-norm / (2 * math.pow (sigma, 2))) # Encuentra convolución gaussiana
        suma = np.sum (gausskernel) # sum
        kernel = gausskernel / suma # normalización
    return kernel

 # Filtro gaussiano
def gauss(img):
    h=img.shape[0]
    w=img.shape[1]
    img1=np.zeros((h,w),np.uint8)
    kernel = gausskernel (3) # Calcular kernel de convolución gaussiana
    for i in range (1,h-1):
        for j in range (1,w-1):
            suma=0
            for k in range(-1,2):
                for l in range(-1,2):
                    suma += img[i + k, j + l] * kernel[k + 1, l + 1] # filtro gaussiano
            img1[i,j]=suma
    return img1

def gaussianFilter(img):
    
    h,w,c = img.shape
    
    kernel_size = 5
    sigma = 1
    
    pad = kernel_size//2
    res = np.zeros((h + 2*pad,w + 2*pad,c), dtype = float)
    res[pad:pad+h,pad:pad+w] = img.copy().astype(float)
    
    # nucleo de filtrado
    kernel = np.zeros((kernel_size,kernel_size), dtype = float)
    
    for x in range(-pad, -pad + kernel_size):
        for y in range(-pad, -pad + kernel_size):
            kernel[y+pad,x+pad] = np.exp(-(x**2 + y**2)/(2*(sigma**2)))
    kernel /= (sigma * np.sqrt(2*np.pi))
    kernel /=  kernel.sum()
    
    tmp = res.copy()
    for y in range(h):
        for x in range(w):
            for ci in range(c):
                res[pad+y,pad+x,ci] = np.sum(kernel*tmp[y:y+kernel_size, x:x+kernel_size, ci])
    
    res = res[pad:pad+h,pad:pad+w].astype(np.uint8)
    
    return res

image = cv.imread("prueba.jpeg")

gaussimg = gaussianFilter(image)

cv.imshow("gaussimg",gaussimg)
