from django.shortcuts import render
from django.http import JsonResponse
from .scripts.picar.test_servo_sanity_check import * 
# Create your views here.
def piCarDash(request):
    return render(request,'picar/picar_dash.html')

def piCarTests(request):
    print(request.POST.get('test'))
    test_servo_rotation()
    return JsonResponse({"result":"good"})
    

