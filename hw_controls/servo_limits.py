import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
frequency = 2000
max_angle = 720                                       ##~Full right position/angle
min_angle = 0                                         ##~Full left position/angle
cur_angle = (max_angle-min_angle)/2       ##~The center position will be the default position/angle
min_dutyCycle = .02
max_dutyCycle = .18
cur_dutyCycle = (max_dutyCycle-min_dutyCycle)/2
cur_dutyCycle = max_dutyCycle
pwm_pin = 12
slope_offset = .02
slope = (max_angle-min_angle)/(max_dutyCycle-min_dutyCycle)    
GPIO.setup(pwm_pin,GPIO.OUT)
pwm_channel = GPIO.PWM(pwm_pin,frequency)
pwm_channel.start(0)
sleep(.5)

for des_pos in range(0,10):
    des_pos = float(des_pos)
    print(des_pos)
    req_dutyCycle = ((des_pos*slope)+slope_offset)*100
    
    pwm_channel.ChangeDutyCycle(1)
    sleep(.1)
    
pwm_channel.ChangeDutyCycle(0)
pwm_channel.stop()