import cv2
import numpy as np

bl = 5
th1 = 100
th2 = 250

capture = cv2.VideoCapture(0)

while True:
    error, frame = capture.read()
    output = frame.copy()
    h, w, _ = frame.shape

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img_gray, (bl,bl))
    # _, img_bin = cv2.threshold(img_blur, th1, th2, cv2.THRESH_BINARY)

    circles = cv2.HoughCircles(
        img_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,
        param1=100,
        param2=40,
        minRadius=1,
        maxRadius=60 #
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x,y,r = circles[0][0]
        cv2.circle(output, (x,y), r, (0,0,255),2) #outline
        cv2.circle(output, (x,y), 2, (0,0,255), 3) #center

    cv2.imshow('circle', output)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

