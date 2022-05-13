import cv2
import sys
import math

im = cv2.imread("test.png",cv2.IMREAD_GRAYSCALE)
_,im = cv2.threshold(im, 128, 255, cv2.THRESH_BINARY)



print("Image original:")
print("Dimensiones: ", im.shape)

# Calculate Moments
moments = cv2.moments(im)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
#for i in range(0,7):
#   huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

for i in range(0,7):
    print("Momento de Hu #", i, ": ", huMoments[i])

im = cv2.resize(im, (60, 60), interpolation = cv2.INTER_AREA)

print("\nImagen reescalada 1:")
print("Dimensiones: ", im.shape)

# Calculate Moments
moments = cv2.moments(im)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
#for i in range(0,7):
#   huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

for i in range(0,7):
    print("Momento de Hu #", i, ": ", huMoments[i])

im = cv2.resize(im, (270, 270), interpolation = cv2.INTER_AREA)

print("\nImagen reescalada 2:")
print("Dimensiones: ", im.shape)

# Calculate Moments
moments = cv2.moments(im)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
#for i in range(0,7):
#   huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

for i in range(0,7):
    print("Momento de Hu #", i, ": ", huMoments[i])

im = cv2.resize(im, (600, 600), interpolation = cv2.INTER_AREA)

print("\nImagen reescalada 3:")
print("Dimensiones: ", im.shape)

# Calculate Moments
moments = cv2.moments(im)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
#for i in range(0,7):
#   huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

for i in range(0,7):
    print("Momento de Hu #", i, ": ", huMoments[i])

im = cv2.resize(im, (1500, 1500), interpolation = cv2.INTER_AREA)

print("\nImagen reescalada 4:")
print("Dimensiones: ", im.shape)

# Calculate Moments
moments = cv2.moments(im)
# Calculate Hu Moments
huMoments = cv2.HuMoments(moments)

# Log scale hu moments
#for i in range(0,7):
#   huMoments[i] = -1* math.copysign(1.0, huMoments[i]) * math.log10(abs(huMoments[i]))

for i in range(0,7):
    print("Momento de Hu #", i, ": ", huMoments[i])
