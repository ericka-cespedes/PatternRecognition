import cv2
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
#import pandas as pd


def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

def calc_fluct(arr):
    fluct = 0
    fluct = max(arr) - min(arr)
    fluct /= abs(np.mean(arr))
    fluct *= 100
    #print(max(arr), "-", min(arr), "/", abs(np.mean(arr)), "*100")
        
    return fluct

def mostrar_histograma(data):
  x_number_list = data[0]
  y_number_list = data[1]

      
  
  plt.title("Histograma")

  plt.xlabel("Número de pixel")
  plt.ylabel("Valor")
  plt.show()

def main():
    im = cv2.imread("test.png",cv2.IMREAD_GRAYSCALE)
    _,im = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)


    res_arr = np.zeros((10, 7), float)
    for res in range(60, 360, 30):
        img_arr = np.zeros((360, 7, 1), float)
        im = cv2.resize(im, (res, res), interpolation = cv2.INTER_AREA)
        for angle in range(1, 361):
            im = rotate_image(im, angle)
            # Calculate Moments
            moments = cv2.moments(im)
            # Calculate Hu Moments
            huMoments = cv2.HuMoments(moments)
            for i in range(0,7):
               huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))
            img_arr[angle-1] = huMoments;
                    
        for moment in range(0, 7):
            #print(calc_fluct(img_arr[:,moment]))
            res_arr[int((res-60)/30)][moment] = calc_fluct(img_arr[:,moment])
            
    
    for i in range(0, 10):
        print("Imagen con resolucion: ", i*30+60)
        for j in range(0, 7):
            print("Momento de Hu #", j+1, " Fluctuacion: ", res_arr[i][j])

    x_values = np.array([])
    y_values1 = np.array([])
    y_values2 = np.array([])
    y_values3 = np.array([])
    y_values4 = np.array([])
    y_values5 = np.array([])
    y_values6 = np.array([])
    y_values7 = np.array([])
    y_values = [y_values1, y_values2, y_values3, y_values4, y_values5, y_values6, y_values7]
    for i in range(0, 10):
      x_values = np.append(x_values, i*30+60)
      for j in range(0, 7):
        y_values[j] = np.append(y_values[j], res_arr[i][j])

    marker_colors = ['royalblue', 'springgreen', 'mediumvioletred', 'gold', 'tomato', 'maroon', 'darkorchid']
    colors = ['cornflowerblue', 'mediumspringgreen', 'magenta', 'yellow', 'salmon', 'firebrick', 'mediumorchid']
    markers = ['o', 's', 'p', 'P', '*', 'X', 'D']

    for i in range(0,7):
      label_name = 'h'+str(i+1)
      plt.plot( x_values, y_values[i], label = label_name, marker=markers[i], markerfacecolor=marker_colors[i], markersize=10, color=colors[i], linewidth=2)

    plt.xlabel('Resolution', fontsize=18)
    plt.ylabel('Fluctuation', fontsize=16)
    plt.legend()
    plt.show()
    
