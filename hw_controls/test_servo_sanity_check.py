import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 50)  # channel=12 frequency=50Hz
p.start(0)
try:
    while 1:
        for dc in range(2, 10, 1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)
        for dc in range(9, 1, -1):
            p.ChangeDutyCycle(dc)
            time.sleep(0.05)
        time.sleep(1)
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
