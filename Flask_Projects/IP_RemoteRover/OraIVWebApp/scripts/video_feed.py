import cv2 
import threading
import numpy as np

"""
fr cv2 install:
   * sudo apt-get install libatlas-base-dev
   * sudo apt-get install libavcodec-dev 
   * sudo apt-get install libavformat-dev 
   * sudo apt-get install libcblas-dev
   * sudo apt-get install libhdf5-dev
   * sudo apt-get install libhdf5-serial-dev
   * sudo apt-get install libjasper-dev 
   * sudo apt-get install libopenjp2-7
   * sudo apt-get install libswscale-dev 
   * sudo apt-get install libv4l-dev
   * sudo apt-get install libxvidcore-dev 
   * sudo apt-get install libx264-dev
   * sudo apt-get install libqtgui4 
   * sudo apt-get install libqt4-test
"""

class CamFeed:
    """
    Provides the PiCam feed to the frontend
    """
    def __init__(self):
        self.contours = []
        self.x_medium = 0
        self.y_medium = 0
        self.obj_dimensions = {}

        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
		#self.frame = cv2.flip(self.frame,flipCode=-1)
        
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()
        del self.video

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def update(self):
        while True:
            #self.frame = cv2.flip(self.frame,flipCode=-1)
            """
            self.hsv_frame = cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)
            self.low_red = np.array([161,155,84])
            self.high_red = np.array([179,255,255])
            self.red_mask = cv2.inRange(self.hsv_frame, self.low_red, self.high_red)

            try:
                self.contours, _ = cv2.findContours(self.red_mask,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                self.contours = sorted(self.contours, key=lambda x:cv2.contourArea(x), reverse = True)
            except Exception:
                _, self.contours, _ = cv2.findContours(self.red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                self.contours = sorted(self.contours, key=lambda x:cv2.contourArea(x), reverse = True)
            
            if len(self.contours) > 0:
                for cnt in self.contours:
                    (x, y, w, h) = cv2.boundingRect(cnt)

                    self.x_medium = int((x + x + w)/2)
                    self.y_medium = int((y + y + h)/2)
                    cv2.rectangle(self.frame, (x,y), (x+w, y+h), (0,255,0), 2)
                    cv2.circle(self.frame,(int(self.x_medium),int(self.y_medium)), int((x+w)/16), (0,255,0),2)
                    self.obj_dimensions['min_x'] = x
                    self.obj_dimensions['max_x'] = x+w
                    self.obj_dimensions['width'] = w
                    self.obj_dimensions['min_y'] = y+h
                    self.obj_dimensions['max_y'] = y
                    self.obj_dimensions['height'] = h
                    self.obj_dimensions['area'] = w*h

                    self.frame_xcenter = self.video.get(3)/2
                    self.object_xcenter = x + w/2
                    break

            cv2.line(self.frame, (self.x_medium,0), (self.x_medium,480), (0,255,0), 2)
            cv2.line(self.frame, (0,self.y_medium), (960,self.y_medium), (0,255,0), 2)
            """
            (self.grabbed, self.frame) = self.video.read()