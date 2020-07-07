from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from .scripts.picar.test_servo_sanity_check import * 
import threading, cv2, time, imutils, datetime
from imutils.video import VideoStream

outputFrame = None
lock = threading.Lock()
isCamOn = False

class piCam(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg',image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

# Create your views here.
def piCarDash(request):
    return render(request,'picar/picar_dash.html')

def piCarTests(request):
    print(request.POST.get('test'))
    test_servo_rotation()
    return JsonResponse({"result":"good"})

def stopCam(request):
    global isCamOn
    isCamOn = False
    return JsonResponse({"action":"stop_camera","result":"success"})

def startCam(request):
    global isCamOn
    isCamOn = True
    #vs = VideoStream(usePiCamera=1).start()
    #vs = VideoStream(src=0).start()
    print(request.POST.get('ctrl'))
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)
    print("trying function")
    startOpenCV(vs)
    print("ran")
    return JsonResponse({"action":"start_camera","result":"success"})

def startOpenCV(vs):
    print("started fnx")
    global outputFrame, lock, isCamOn
    print("got global")
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
    cv2.destroyAllWindows()

def piCamFeed(request):
    cam = piCam()
    return StreamingHttpResponse(gen(cam),content_type="multipart/x-mixed-replace;boundary=frame")

def gen(cam):
    while True:
        frame = cam.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
