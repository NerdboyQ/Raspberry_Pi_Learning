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
from adafruit_motor import *


class OraIV:

    def __init__(self):
        self._delay = 0.5 
        self._motor_ctrlr = MotorKit(i2c=board.I2C())
        self._f_l_motor = self._motor_ctrlr.motor4
        self._f_r_motor = self._motor_ctrlr.motor3
        self._b_r_motor = self._motor_ctrlr.motor1
        self._b_l_motor = self._motor_ctrlr.motor2

    def __del__(self):
        self.stop_motors()
        del self._motor_ctrlr

    def drive_forward(self, speed):
        self._b_r_motor.throttle = speed
        self._b_l_motor.throttle = speed
        self._f_r_motor.throttle = speed
        self._f_l_motor.throttle = speed

    def drive_reverse(self, speed):
        self._b_r_motor.throttle = -speed
        self._b_l_motor.throttle = -speed
        self._f_r_motor.throttle = -speed
        self._f_l_motor.throttle = -speed

    def drive_left(self, speed):
        self._b_r_motor.throttle = -speed
        self._b_l_motor.throttle = speed
        self._f_r_motor.throttle = speed
        self._f_l_motor.throttle = -speed

    def drive_right(self, speed):
        self._b_r_motor.throttle = speed
        self._b_l_motor.throttle = -speed
        self._f_r_motor.throttle = -speed
        self._f_l_motor.throttle = speed

    def drift_fleft(self, speed):
        self._b_r_motor.throttle = 0.75
        self._b_l_motor.throttle = -0.75
        self._f_r_motor.throttle = 0.75
        self._f_l_motor.throttle = .5

    def drift_fright(self, speed):
        self._b_r_motor.throttle = -0.75
        self._b_l_motor.throttle = 0.75
        self._f_r_motor.throttle = .5
        self._f_l_motor.throttle = 0.75

    def drift_rleft(self, speed):
        self._b_r_motor.throttle = -0.5
        self._b_l_motor.throttle = -0.75
        self._f_r_motor.throttle = 0.75
        self._f_l_motor.throttle = -0.75

    def drift_rright(self, speed):
        self._b_r_motor.throttle = -0.75
        self._b_l_motor.throttle = -0.5
        self._f_r_motor.throttle = -0.75
        self._f_l_motor.throttle = 0.75

    def rotate_cw(self, speed):
        self._b_r_motor.throttle = -speed
        self._b_l_motor.throttle = speed
        self._f_r_motor.throttle = -speed
        self._f_l_motor.throttle = speed

    def rotate_ccw(self, speed):
        self._b_r_motor.throttle = speed
        self._b_l_motor.throttle = -speed
        self._f_r_motor.throttle = speed
        self._f_l_motor.throttle = -speed

    def diagl_forward(self, speed):
        self._b_l_motor.throttle = speed
        self._f_r_motor.throttle = speed

    def diagl_reverse(self, speed):
        self._b_r_motor.throttle = -speed
        self._f_l_motor.throttle = -speed

    def diagr_forward(self, speed):
        self._b_r_motor.throttle = speed
        self._f_l_motor.throttle = speed

    def diagr_reverse(self, speed):
        self._b_l_motor.throttle = -speed
        self._f_r_motor.throttle = -speed

    def stop_motors(self):
        self._b_r_motor.throttle = 0
        self._b_l_motor.throttle = 0
        self._f_r_motor.throttle = 0
        self._f_l_motor.throttle = 0

    def test_motors(self):
        self._f_l_motor.throttle = 1.0
        time.sleep(1)
        self._f_r_motor.throttle = 1.0
        time.sleep(1)
        self._b_l_motor.throttle = 1.0
        time.sleep(1)
        self._b_r_motor.throttle = 1.0
        time.sleep(1)
        self.stop_motors()

    def test_movements(self, speed):
        # Forward/Reverse
        self.drive_forward(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        self.drive_reverse(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        # Left/Right
        self.drive_left(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        self.drive_right(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        # Diagnal Diamond
        self.diagl_forward(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        self.diagr_forward(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        self.diagr_reverse(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        self.diagl_reverse(speed)
        time.sleep(self._delay)
        self.stop_motors()
        time.sleep(self._delay)
        # Diagnal Diamond
        self.rotate_ccw(speed)
        time.sleep(self._delay*2)
        self.stop_motors()
        time.sleep(self._delay)
        self.rotate_cw(speed)
        time.sleep(self._delay*2)
        self.stop_motors()

if __name__ == "__main__":
    ora = OraIV()