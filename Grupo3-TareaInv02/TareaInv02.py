import cv2
import sys
import math
import numpy as np

def has_inverse_map(a, b, c, d):
  if (b*c-a*d) == 0: 
    return False
  else:
    return True


def w_plane_representation(img, a, b, c, d):
  height = img.shape[0]
  width = img.shape[1]
  w_plane = np.zeros((height,width,3), np.uint8)
  for i in range(height):
    for j in range(width):
      z = complex(j, i)
      w = (a*z + b) / (c*z + d)
      if w.imag < height and w.real < width:        
        w_plane[int(w.imag), int(w.real)] = img[i, j]
      
  
  cv2.imshow('w_plane', w_plane)
  

def lineal_mapping_demonstration(img, a, b):
  c = 0
  d = 1
  w_plane_representation(img, a, b, c, d)

def map_save(img, a, b, c, d):
  if not has_inverse_map(a, b, c, d):
    sys.exit("Las constantes seleccionadas no tienen mapeo inverso.")

  height = img.shape[0]
  width = img.shape[1]
  w_plane = np.zeros((height,width,3), np.uint8)
  for i in range(height):
    for j in range(width):
      z = complex(j, i)
      w = (a*z + b) / (c*z + d)
      if w.imag < height and w.real < width:        
        w_plane[int(w.imag), int(w.real)] = img[i, j]
    
  cv2.imwrite('imagen2.jpg', w_plane)
  return w_plane
  

def obtain_inverse_map(img, a, b, c, d):
  height = img.shape[0]
  width = img.shape[1]
  inverse_plane = np.zeros((height,width,3), np.uint8)
  for i in range(height):
    for j in range(width):
      w = complex(j, i)
      z = (-d*w + b) / (c*w - a)
      if z.imag.is_integer() and z.real.is_integer():      
        inverse_plane[int(z.imag), int(z.real)] = img[i, j]
  
  cv2.imwrite('imagen3.jpg', inverse_plane)
  return inverse_plane


def interpolation_n_4(img, a, b, c, d):
  height = img.shape[0]
  width = img.shape[1]
  new_plane = np.zeros((height,width,3), dtype='float')
  inv_plane = obtain_inverse_map(img, a, b, c, d)
  sum = np.zeros(3, dtype='float')
  for i in range(height):
    for j in range(width):      
      new_plane[i, j] = img[i, j]
      if np.sum(img[i, j]) == 0.0:
        w = complex(j, i)
        z = (-d*w + b) / (c*w - a)
        temp_i = int(z.imag)
        temp_j = int(z.real)
        if temp_j+1 >= width:
          temp_j = width-2         
        if temp_i+1 >= height:
          temp_i = height-2
        if temp_i-1 < 0:
          temp_i = 1
        if temp_j-1 < 0:
          temp_j = 1
        
        sum = inv_plane[temp_i-1,temp_j] + inv_plane[temp_i, temp_j-1] +  inv_plane[temp_i, temp_j+1] + inv_plane[temp_i+1, temp_j]
        sum = sum / [4, 4, 4]
        new_plane[i, j] = sum    
      


  cv2.imwrite('imagen4.jpg', new_plane)
  return new_plane


def interpolation_n_8(img, a, b, c, d):
  height = img.shape[0]
  width = img.shape[1]
  new_plane = np.zeros((height,width,3), dtype='float')
  inv_plane = obtain_inverse_map(img, a, b, c, d)
  sum = np.zeros(3, dtype='float')
  for i in range(height):
    for j in range(width):
      new_plane[i, j] = img[i, j]
      if np.sum(img[i, j]) == 0.0:
        w = complex(j, i)
        z = (-d*w + b) / (c*w - a)
        temp_i = int(z.imag)
        temp_j = int(z.real)
        if temp_j+1 >= width:
          temp_j = width-2         
        if temp_i+1 >= height:
          temp_i = height-2
        if temp_i-1 < 0:
          temp_i = 1
        if temp_j-1 < 0:
          temp_j = 1

        sum = inv_plane[temp_i-1, temp_j-1] + inv_plane[temp_i-1, temp_j] + inv_plane[temp_i, temp_j-1] + inv_plane[temp_i, temp_j+1] + inv_plane[temp_i-1, temp_j+1] + inv_plane[temp_i+1,temp_j] + inv_plane[temp_i+1, temp_j-1] + inv_plane[temp_i+1,temp_j+1]
        sum = sum / [8, 8, 8]
        new_plane[i, j] = sum
      
      
  cv2.imwrite('imagen5.jpg', new_plane)
  return new_plane

#Gauss
def gaussianFilter(img):
    
    h,w,c = img.shape
    
    kernel_size = 5
    sigma = 3
    
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


def main():
  imgR = cv2.imread('Manuel_A_prueba00.jpeg')  
  if imgR is None:
    sys.exit("No se pudo leer la imagen.")
  a = 2
  b = 0
  c = 0
  d = 1

  print('Se quitaron los imshow() para que no tarde tanto, las imagenes se guardan en la carpeta.')
  
  new_image = map_save(imgR, a, b, c, d)
  #cv2.imshow('imagen2', new_image)
  print('El punto 2 ha terminado.')
  
  plane_z = obtain_inverse_map(new_image, a, b, c, d)
  #cv2.imshow('imagen3', plane_z)
  print('El punto 3 ha terminado.')
  
  inter_4 = interpolation_n_4(new_image, a, b, c, d)
  #cv2.imshow('imagen4', inter_4)
  print('El punto 4 ha terminado.')

  inter_8 = interpolation_n_8(new_image, a, b, c, d)
  #cv2.imshow('imagen5', inter_8)
  print('El punto 5 ha terminado.')

  gauss6 = gaussianFilter(new_image)
  #cv2.imshow('imagen6', gauss6)
  cv2.imwrite('imagen6.jpg', gauss6)
  print('El punto 6 ha terminado.')

  gauss7 = gaussianFilter(plane_z)
  #cv2.imshow('imagen7', gauss7)
  cv2.imwrite('imagen7.jpg', gauss7)
  print('El punto 7 ha terminado.')

  print('El programa ha terminado.')

main()
