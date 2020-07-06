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
    ##~The loop below will find our red objects and place boxes around them, however due to the break
    ##~command, it will stop with the first (and largest) red object detected in the frame.
    
    if len(contours) > 0:
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
		
            x_medium = int((x + x +w)/2)
            y_medium = int((y + y + h)/2)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.circle(frame,(int(x_medium),int(y_medium)), int((x+w)/16),(0,255,0),2)
            #|cv2.rectangle(frame, (0,0), (50, 50), (0,255,0), 2)
            obj_dimensions['min_x'] = x
            obj_dimensions['max_x'] = x+w
            obj_dimensions['width'] = w
            obj_dimensions['min_y'] = y+h
            obj_dimensions['max_y'] = y
            obj_dimensions['height'] = h
            obj_dimensions['area'] = w*h
            print("-"*100)
            print("center x - point: " +str(vid.get(3)/2))
            frame_xcenter = cvid.get(3)/2
            object_xcenter = x + w/2
            steering_pos = find_and_center(steering_pos,object_xcenter,frame_xcenter,s)
            break
    else:
        print("Object not detected")
    ##~Below, just to make it easier for tracking, a vertical & horizontal line will be created that will cross
    ##~through the center of the detected object. This line can later be used to track how close the object is 
    ##~to the center of the frame. 
    cv2.line(frame, (x_medium,0), (x_medium,480), (0,255,0),2)
    cv2.line(frame, (0,y_medium), (960,y_medium), (0,255,0),2)

    cv2.imshow('Frame',frame)

    key = cv2.waitKey(1)
    if key == 115:
        break

vid.release()
cv2.destroyAllWindows()
