import cv2
import numpy as np

bl = 5
th1 = 100
th2 = 250

# colors 
clr_line = (0,0,255)
clr_outl = (0,0,255)
clr_cent = (0,0,255)
clr_txt = (0,0,0)
font = cv2.FONT_HERSHEY_SIMPLEX
thick1 = 2

on_left = False
left_count = 0
right_count = 0

capture = cv2.VideoCapture(0)

while True:
    error, frame = capture.read()
    output = frame.copy()
    h, w, _ = frame.shape

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img_gray, (bl,bl))


    circles = cv2.HoughCircles(
        img_blur,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=100,
        param1=100,
        param2=40,
        minRadius=1,
        maxRadius=60
    )
    if circles is not None:
        circles = np.uint16(np.around(circles))
        x,y,r = circles[0][0]
        cv2.circle(output, (x,y), r, clr_outl, thick1) #outline
        cv2.circle(output, (x,y), 2, clr_cent, thick1) #center
        
        if x < (w // 2): 
            if on_left == False:
                left_count += 1
                on_left = True
        else:
            if on_left == True:
                right_count += 1
                on_left = False

    cv2.line(output, (w // 2, 0), (w // 2, h), clr_line, thick1)
    cv2.putText(output, str(left_count), (100, 100), font, 1, clr_txt, thick1)
    cv2.putText(output, str(right_count), (w-100, 100), font, 1, clr_txt, thick1)
    

    cv2.imshow('circle', output)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

