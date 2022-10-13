"""
Current Rover orientation

--Front---
M4  |   M3
-L------R-
M2  |   M1
---Back---

"""


import time
import board
from adafruit_motorkit import MotorKit

def drive_forward(speed):
    kit.motor1.throttle = speed
    kit.motor2.throttle = speed
    kit.motor3.throttle = speed
    kit.motor4.throttle = speed

def drive_reverse(speed):
    kit.motor1.throttle = -speed
    kit.motor2.throttle = -speed
    kit.motor3.throttle = -speed
    kit.motor4.throttle = -speed

def drive_left(speed):
    kit.motor1.throttle = -speed
    kit.motor2.throttle = speed
    kit.motor3.throttle = speed
    kit.motor4.throttle = -speed

def drive_right(speed):
    kit.motor1.throttle = speed
    kit.motor2.throttle = -speed
    kit.motor3.throttle = -speed
    kit.motor4.throttle = speed

def drift_fleft(speed):
    kit.motor1.throttle = 0.75
    kit.motor2.throttle = -0.75
    kit.motor3.throttle = 0.75
    kit.motor4.throttle = .5

def drift_fright(speed):
    kit.motor1.throttle = -0.75
    kit.motor2.throttle = 0.75
    kit.motor3.throttle = .5
    kit.motor4.throttle = 0.75

def drift_rleft(speed):
    kit.motor1.throttle = -0.5
    kit.motor2.throttle = -0.75
    kit.motor3.throttle = 0.75
    kit.motor4.throttle = -0.75

def drift_rright(speed):
    kit.motor1.throttle = -0.75
    kit.motor2.throttle = -0.5
    kit.motor3.throttle = -0.75
    kit.motor4.throttle = 0.75

def rotate_cw(speed):
    kit.motor1.throttle = -speed
    kit.motor2.throttle = speed
    kit.motor3.throttle = -speed
    kit.motor4.throttle = speed

def rotate_ccw(speed):
    kit.motor1.throttle = speed
    kit.motor2.throttle = -speed
    kit.motor3.throttle = speed
    kit.motor4.throttle = -speed

def diagl_forward(speed):
    kit.motor2.throttle = speed
    kit.motor3.throttle = speed

def diagl_reverse(speed):
    kit.motor1.throttle = -speed
    kit.motor4.throttle = -speed

def diagr_forward(speed):
    kit.motor1.throttle = speed
    kit.motor4.throttle = speed

def diagr_reverse(speed):
    kit.motor2.throttle = -speed
    kit.motor3.throttle = -speed

def stop_motors():
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0
    kit.motor3.throttle = 0
    kit.motor4.throttle = 0

def test_motors():
    kit.motor1.throttle = 1.0
    time.sleep(1)
    kit.motor2.throttle = 1.0
    time.sleep(1)
    kit.motor3.throttle = 1.0
    time.sleep(1)
    kit.motor4.throttle = 1.0
    time.sleep(1)

def test_movements(speed):
    # Forward/Reverse
    drive_forward(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    drive_reverse(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    # Left/Right
    drive_left(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    drive_right(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    # Diagnal Diamond
    diagl_forward(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    diagr_forward(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    diagr_reverse(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    diagl_reverse(speed)
    time.sleep(delay)
    stop_motors()
    time.sleep(delay)
    # Diagnal Diamond
    rotate_ccw(speed)
    time.sleep(delay*2)
    stop_motors()
    time.sleep(delay)
    rotate_cw(speed)
    time.sleep(delay*2)
    stop_motors()

kit = MotorKit(i2c=board.I2C())
delay = 0.5
#test_movements(.5)
"""
drift_rleft(0.5)
time.sleep(delay)
stop_motors()
time.sleep(delay)
drift_rright(0.5)
time.sleep(delay)
stop_motors()
"""
