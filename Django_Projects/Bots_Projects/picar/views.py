from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from .scripts.picar.test_servo_sanity_check import * 
import threading, cv2, time, imutils, datetime
import numpy as np
from imutils.video import VideoStream

outputFrame = None
lock = threading.Lock()
isCamOn = False
cam = None

class piCam(object):
	def __init__(self):
		self.contours = []
		self.x_medium = 0
		self.y_medium = 0
		self.obj_dimensions = {}

		self.video = cv2.VideoCapture(0)
		(self.grabbed, self.frame) = self.video.read()
		self.frame = cv2.flip(self.frame,flipCode=-1)



		threading.Thread(target=self.update, args=()).start()

	def __del__(self):
		self.video.release()

	def get_frame(self):
		image = self.frame
		ret, jpeg = cv2.imencode('.jpg',image)
		return jpeg.tobytes()

	def update(self):
		while True:
			self.frame = cv2.flip(self.frame,flipCode=-1)
			
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

			(self.grabbed, self.frame) = self.video.read()

# Create your views here.
def piCarDash(request):
    return render(request,'picar/picar_dash.html')

def piCarTests(request):
    print(request.POST.get('test'))
    test_servo_rotation()
    return JsonResponse({"result":"good"})

def stopCam(request):
    global isCamOn, cam
    isCamOn = False
    if cam != None:
        del cam
    return JsonResponse({"action":"stop_camera","result":"success"})

def startCam(request):
    global isCamOn
    isCamOn = True
    if cam == None:
        cam = piCam()
    #vs = VideoStream(usePiCamera=1).start()
    #vs = VideoStream(src=0).start()
    print(request.POST.get('ctrl'))
    print("trying function")
    print("ran")
    return JsonResponse({"action":"start_camera","result":"success"})

def startOpenCV(vs):
    print("started fnx")
    global outputFrame, lock, isCamOn
    print("got global")
    '''
    while isCamOn == True:
        print("entered while loop")
        _, frame = vs.read()
        print("read frame")
        frame = cv2.flip(frame,flipCode=-1)
        print("isCamOn status: ", str(isCamOn))
        ##test line
        frame_encode = cv2.imencode('.jpg', frame)[1].tostring()
        print("frame encode:: ",frame_encode)
        #cv2.imshow('Frame',frame)
        with lock:
            outputFrame = frame.copy()
        if isCamOn == False:
            break
    vs.release()
    cv2.destroyAllWindows()'''

def piCamFeed(request):
    global cam
    #if isCamOn:
    cam = piCam()
    return StreamingHttpResponse(gen(cam),content_type="multipart/x-mixed-replace;boundary=frame")

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
