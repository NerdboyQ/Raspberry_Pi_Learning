import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class servo:

    def __init__(self):
        self._frequency = 50
        self._max_angle = 120                                       ##~Full right position/angle
        self._min_angle = 0                                         ##~Full left position/angle
        self._cur_angle = (self._max_angle-self._min_angle)/2       ##~The center position will be the default position/angle
        self._min_dutyCycle = .05
        self._max_dutyCycle = .10
        self._cur_dutyCycle = (self._max_dutyCycle-self._min_dutyCycle)/2
        self._pwm_pin = 12
        self._slope_offset = .05
        
        GPIO.setup(self._pwm_pin,GPIO.BOARD)
        self._pwm_channel = GPIO.PWM(self._pwm_pin,self._frequency)
        self._pwm_channel.start((self._cur_duty_cycle)*100)
        self.slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self.max_angle,self.min_angle)
        print("Servo_Created with slope: " +str(self.slope))

    def calculate_slope(self,y2,y1,x2,x1):
        slope = (y2-y1)/(x2-x1)
        return slope

    def steer(self,des_pos):
        des_pos = float(des_pos)
        req_dutyCycle = ((des_pos*self.slope)+self.slope_offset)*100
        self.pwm_channel.ChangeDutyCycle(req_dutCycle)
        print(req_dutyCycle)
        
    def kill_servo(self):
        self.pwm_channel.stop()

    #getting the value
    @property
    def max_angle(self):
        return self._max_angle
    @max_angle.setter
    def max_angle(self,val):
        self._max_angle = val
        self.slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self._max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._max_angle
    
    @property
    def min_angle(self):
        return self._min_angle
    @min_angle.setter
    def min_angle(self,val):
        self._min_angle = val
        self.slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self.max_angle,self._min_angle)
        print("new slope : " +str(self.slope))
        return self._min_angle
    
    @property
    def max_dutyCycle(self):
        return self._max_dutyCycle
    @max_dutyCycle.setter
    def max_dutyCycle(self,val):
        self._max_dutyCycle = val
        self.slope = self.calculate_slope(self._max_dutyCycle,self.min_dutyCycle,self.max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._max_dutyCycle
    
    @property
    def min_dutyCycle(self):
        return self._min_dutyCycle
    @min_dutyCycle.setter
    def min_dutyCycle(self,val):
        self._max_dutyCycle = val
        self.slope = self.calculate_slope(self.max_dutyCycle,self._min_dutyCycle,self.max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._min_dutyCycle
       
    @property
    def pwm_pin(self):
        return self._pwm_pin
    @pwm_pin.setter
    def pwm_pin(self,val):
        self.pwm_channel.stop()
        self._pwm_pin = val
        GPIO.setup(self._pwm_pin,GPIO.BOARD)
        self.pwm_channel = GPIO.PWM(self._pwm_pin,self.frequency)
        self.pwm_channel.start((self.cur_duty_cycle)*100)
        return self._pwm_pin
    
    @property
    def slope_offset(self):
        return self._slope_offset
    
    @property 
    def frequency(self):
        return self._frequency
    @frequency.setter 
    def frequency(self,val):
        self._frequency = val
        self.pwm_channel.ChangeFrequency(val)
        return self._frequency
    
    @property
    def cur_angle(self):
        return self._cur_angle
    @cur_angle.setter
    def cur_angle(self,val):
        self._cur_angle = val
        self.steer(self,val)
        return self._cur_angle
    
    @property
    def cur_dutyCycle(self):
        return self._cur_dutyCycle

