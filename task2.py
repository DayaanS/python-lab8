import cv2
import numpy as np

bl = 5
bin1 = 100
bin2 = 250

capture = cv2.VideoCapture(0)

while True:
    error, frame = capture.read()
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img_gray, (bl,bl))
    _, bin_frame = cv2.threshold(img_blur, bin1, bin2, cv2.THRESH_BINARY)

    cv2.imshow('camera', bin_frame)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

