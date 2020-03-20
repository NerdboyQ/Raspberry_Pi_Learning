import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class servo:

    def __init__(self):
        self._max_angle = 120
        self._min_angle = 0
        self._cur_angle = 60
        self._min_dutyCycle = .05
        self._max_dutyCycle = .10
        self._cur_dutyCycle = .075
        self._pwm_pin = 12
        self._slope_offset = .05
        
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
    
    @property
    def min_angle(self):
        return self._min_angle
     
    @property
    def cur_angle(self):
        return self._cur_angle
    
    @property
    def max_dutyCycle(self):
        return self._max_dutyCycle
    
    @property
    def min_dutyCycle(self):
        return self._min_dutyCycle

    @property
    def cur_dutyCycle(self):
        return self._cur_dutyCycle
    
    @property
    def pwm_pin(self):
        return self._pwm_pin
    
    @property
    def slope_offset(self):
        return self._slope_offset
