import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class servo:
    slope = 0
    max_angle = 120
    min_angle = 0
    cur_angle = 60
    min_dutyCycle = .05
    max_dutyCycle = .10
    cur_dutyCycle = .075
    pwm_pin = 12
    slope_offset = .05

    def __init__(self):
        self._max_angle = 120
        self.slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self.max_angle,self.min_angle)
        print("Servo_Created with slope: " +str(self.slope))

    def calculate_slope(self,y2,y1,x2,x1):
        slope = (y2-y1)/(x2-x1)
        return slope

    def steer(self,des_pos):
        des_pos = float(des_pos)
        req_dutyCycle = ((des_pos*self.slope)+self.slope_offset)*100
        print(req_dutyCycle)

    #getting the value
    @property
    def max_angle(self):
        return self._max_angle

