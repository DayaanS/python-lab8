import cv2
import numpy as np

BL = 5
TH1 = 100
TH2 = 250

CLR_LINE = (0,0,255)
CLR_OUTL = (0,0,255)
CLR_TXT = (0,0,255)
FONT = cv2.FONT_HERSHEY_SIMPLEX
THICKNESS = 2

on_left = False
left_count = 0
right_count = 0

capture = cv2.VideoCapture(0)
fly = cv2.imread('fly64.png', cv2.IMREAD_UNCHANGED)


def overlay(bg, ovrl, x, y):
    oh, ow, _ = ovrl.shape
    ovrl_alpha = ovrl[:,:,3]/255.0
    bg_alpha = 1.0 - ovrl_alpha
    
    for c in range(0,3):
        bg[y-oh//2:y+oh//2, x-ow//2:x+ow//2, c] = (ovrl_alpha * ovrl[:, :, c] + \
                                                   bg_alpha * bg[y-oh//2:y+oh//2, x-ow//2:x+ow//2, c])


def detect_circles(img):
    circles = cv2.HoughCircles(
        img,
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
        cv2.circle(output, (x,y), r, CLR_OUTL, THICKNESS)
        overlay(output, fly, x, y)
        return x


while True:
    error, frame = capture.read()
    output = frame.copy()
    h, w, _ = frame.shape

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.blur(img_gray, (BL,BL))

    x = detect_circles(img_blur)

    if x:
        if x < (w // 2): 
            if not on_left:
                left_count += 1
                on_left = True
        else:
            if on_left or (right_count == 0 and left_count == 0):
                right_count += 1
                on_left = False
    cv2.line(output, (w // 2, 0), (w // 2, h), CLR_LINE, THICKNESS)
    cv2.putText(output, str(left_count), (100, 100), FONT, 1, CLR_TXT, THICKNESS)
    cv2.putText(output, str(right_count), (w-100, 100), FONT, 1, CLR_TXT, THICKNESS)
    
    cv2.imshow('circle detector', output)
    
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

