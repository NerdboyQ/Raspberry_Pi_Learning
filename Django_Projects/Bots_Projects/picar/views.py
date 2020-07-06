from django.shortcuts import render
from django.http import JsonResponse
from .scripts.picar.test_servo_sanity_check import * 
import threading, cv2, time, imutils, datetime
from imutils.video import VideoStream

outputFrame = None
lock = threading.Lock()
isCamOn = False

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
    isCamOn = True
    #vs = VideoStream(usePiCamera=1).start()
    #vs = VideoStream(src=0).start()
    vs = cv2.VideoCapture(0)
    time.sleep(2.0)
    startOpenCV(vs,isCamOn)
    return JsonResponse({"action":"start_camera","result":"success"})

def startOpenCV(vs,isCamOn):
    global outputFrame, lock
    while True:
        _, frame = vs.read()
        frame = cv2.flip(frame,flipCode=-1)
        cv2.imshow('Frame',frame)
        with lock:
            outputFrame = frame.copy()
        if isCamOn == False:
            break
    vs.release()
    cv2.destroyAllWindows()
