import cv2 
import numpy as np 

img = cv2.imread('variant-6.png')

w, h, _ = img.shape

stretch = cv2.resize(img, (w*2,h))

cv2.imshow('task1', stretch)
cv2.waitKey(0)