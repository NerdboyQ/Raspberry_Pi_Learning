import cv2, time, os, threading
import numpy as np

vid = cv2.VideoCapture(0)
countours = []
x_medium = 0
y_medium = 0
obj_dimensions = {}
while True:
    _, frame = vid.read()
    frame = cv2.flip(frame,flipCode=-1)
    hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    low_red = np.array([161,155,84])
    high_red = np.array([179,255,255])

    red_mask = cv2.inRange(hsv_frame, low_red, high_red)

    try:
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)
    except Exception:
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)


    cv2.imshow('Frame',frame)

    key = cv2.waitKey(1)
    if key == 115:
        break

vid.release()
cv2.destroyAllWindows()
