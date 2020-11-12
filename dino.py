import cv2 as cv
import numpy as np
from pynput.keyboard import Key, Controller
import time

def f(x):
    return x

kb=Controller()

cv.namedWindow("video")
cv.createTrackbar('A','video',150,300,f)
cv.createTrackbar('B','video',170,300,f)
# right rotation decreases angle
cap=cv.VideoCapture(0)
new=2.4
old=2.4
while(cap.isOpened()):
    ret, frame=cap.read()
    gray=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    a=cv.getTrackbarPos('A','video')
    b=cv.getTrackbarPos('B','video')
    canny=cv.Canny(gray,a,b)
    lines=cv.HoughLines(canny, 1,np.pi/180,50)
    key=0
    for line1 in lines:
        for line2 in lines:
            if(1.56<=line1[0][1]-line2[0][1]<=1.58):
                rho,theta = line1[0]
                new,old=theta,new
                print(line1[0])
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                key=1
        if(key==1):
            break
    # if(new>old+0.1):
    #     kb.press(Key.down)
    #     time.sleep(0.1)
    #     kb.release(Key.down)
    if(old>new+0.02):
        kb.press(Key.up)
        time.sleep(0.1)
        kb.release(Key.up)
    cv.imshow("video",frame)
    if(cv.waitKey(1)==ord('q')):
        break
cap.release()
cv.destroyAllWindows()