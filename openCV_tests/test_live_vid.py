##~Author : Princton C. Brennan
##~Created : March 6th, 2020
##~   Compatibilty : Python 3.5+
##~   Requirements (Python): opencv-python & numpy 
##~   Hardware : PiCamera or another Camera 
##~
##~ NOTE:: There are other pre-requisites that are non-python related, 
##~        please see the ReadMe file for those required steps.
##~
##~Code Functionality : Color-based Object Tracking w/ live camera feed 

import cv2 
import numpy as np
 
cap = cv2.VideoCapture(0)

pos = 90 # degrees center for servo

##~ These variables are created below, but because of the try/except condition
##~ they may appear as 'undefined'. So we give them default values
countours = []
x_medium = 0
y_medium = 0

while True:
    _, frame = cap.read() ##~ This line creates an instance of the frame to display the camera feed
    
    ##~This converts the color space of the frame from Blue/Green/Red -> Hue/Saturation/Value
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
     
    ##~The lines below define a range of reds the 'lowest' hue of red tot he 'highest' to ensure we can capture
    ##~as many types of red in the frame as possible.
    low_red = np.array([161,155,84])
    high_red = np.array([179,255,255])
    
    ##~The line below masks every color that isn't within the red range we defined. Anything in red will appear
    ##~as whire in the frame created below, while everything else will appear black. This makes it easier to 
    ##~find the "contours" or where the edges of our red object(s) meet the background (non-red objects). 
    red_mask = cv2.inRange(hsv_frame, low_red, high_red)
    
    ##~The lines below will try to find the contours of our red objects
    ##~ NOTE:: There are two attempts made to compensate for version differences in opencv,
    ##~        and the associated system files, versions
    try:
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)
    except Exception:
        _, contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)
    
    ##~The loop below will find our red objects and place boxes around them, however due to the break
    ##~command, it will stop with the first (and largest) red object detected in the frame.
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        x_medium = int((x + x +w)/2)
        y_medium = int((y + y + h)/2)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        cv2.circle(frame,(int(x_medium),int(y_medium)), int((x+w)/16),(0,255,0),2)
        break
    
    ##~Below, just to make it easier for tracking, a vertical & horizontal line will be created that will cross
    ##~through the center of the detected object. This line can later be used to track how close the object is 
    ##~to the center of the frame. 
    cv2.line(frame, (x_medium,0), (x_medium,480), (0,255,0),2)
    cv2.line(frame, (0,y_medium), (960,y_medium), (0,255,0),2)
    
    ##~The lines below show the live feed of the full color frame and the masked red fram (appears black and white).
    cv2.imshow('Frame', frame)
    cv2.imshow('mask', red_mask)

    ##~Because this code lives in a continuous while loop, a key stroke check has been included below to quit this
    ##~code when the 's' key has been pressed. '115' is the number representation of the ASCII character 's'.
    key = cv2.waitKey(1)
    if key == 115:
        break

##~Finally we will stop the camera capture session after quitting the loop and closing all the frame windows. 
cap.release()
cv2.destroyAllWindows()
