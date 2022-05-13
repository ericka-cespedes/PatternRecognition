import numpy as np
import cv2
import sys

#define kernel convolution function
# with image X and filter F
def convolve(X, F):
    # height and width of the image
    X_height = X.shape[0]
    X_width = X.shape[1]
    
    # height and width of the filter
    F_height = F.shape[0]
    F_width = F.shape[1]
    
    H = (F_height - 1) // 2
    W = (F_width - 1) // 2
    
    #output numpy matrix with height and width
    out = np.zeros((X_height, X_width))
    #iterate over all the pixel of image X
    for i in np.arange(H, X_height-H):
        for j in np.arange(W, X_width-W):
            sum = 0
            #iterate over the filter
            for k in np.arange(-H, H+1):
                for l in np.arange(-W, W+1):
                    #get the corresponding value from image and filter
                    a = X[i+k, j+l]
                    w = F[H+k, W+l]
                    sum += (w * a)
            out[i,j] = sum
    #return convolution  
    return out

def main():
    image = cv2.imread('puntaLeona2.jpg', cv2.IMREAD_GRAYSCALE)
    if image is None:
        sys.exit("No se pudo leer la imagen.")
        
    #define horizontal and Vertical sobel kernels
    Gx = np.array([[-1, 0, 1],[-2, 0, 2],[-1, 0, 1]])
    Gy = np.array([[-1, -2, -1],[0, 0, 0],[1, 2, 1]])
    
    #normalizing the vectors
    sob_x = convolve(image, Gx) / 8.0
    sob_y = convolve(image, Gy) / 8.0

    #calculate the gradient magnitude of vectors
    sob_out = np.sqrt(np.power(sob_x, 2) + np.power(sob_y, 2))
    # mapping values from 0 to 255
    sob_out = (sob_out / np.max(sob_out)) * 255

    #output images
    cv2.imwrite('out.jpeg', sob_out)
    cv2.imshow('out', sob_out)
