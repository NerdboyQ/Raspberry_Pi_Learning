import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
frequency = 60
max_angle = 360                                       ##~Full right position/angle
min_angle = 0                                         ##~Full left position/angle
cur_angle = (max_angle-min_angle)/2       ##~The center position will be the default position/angle
min_dutyCycle = 2
max_dutyCycle = 18
cur_dutyCycle = (max_dutyCycle-min_dutyCycle)/2
cur_dutyCycle = max_dutyCycle
pwm_pin = 12
slope_offset = 2
slope = (max_angle-min_angle)/(max_dutyCycle-min_dutyCycle)    
GPIO.setup(pwm_pin,GPIO.OUT)
pwm_channel = GPIO.PWM(pwm_pin,frequency)
pwm_channel.start(0)
sleep(.5)

for des_pos in range(0,420,60):
    des_pos = float(des_pos)
    print(des_pos)
    req_dutyCycle = ((des_pos*slope)+slope_offset)*100
    pwm_channel.ChangeDutyCycle(2+(des_pos/18))
    print(2+(des_pos/18))
    sleep(1)
    pwm_channel.ChangeDutyCycle(0)
    sleep(1)
    
pwm_channel.ChangeDutyCycle(0)
pwm_channel.stop()
GPIO.cleanup()