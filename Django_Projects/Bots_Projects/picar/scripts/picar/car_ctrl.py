import RPi.GPIO as GPIO
from time import sleep


##~ For property setter methods to work, the class must inherent the 'object' class
##~ NOTE: This class is still in development
class driver(object):
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self._frequency = 50
        self._cur_dutyCycle = .18
        self._min_dutyCycle = .18
        self._max_dutyCycle = .18
        self._drive_fwd_pin = 16
        self._drive_rvr_pin = 18

        GPIO.setup(self._drive_fwd_pin,GPIO.OUT)
        GPIO.setup(self._drive_rvr_pin,GPIO.OUT)
        self._drive_fwd_pwm_channel = GPIO.PWM(self._drive_fwd_pin,self._frequency)
        self._drive_fwd_pwm_channel.start(0)
        sleep(.5)
        self._drive_rvr_pwm_channel = GPIO.PWM(self._drive_rvr_pin,self._frequency)
        self._drive_rvr_pwm_channel.start(0)
        sleep(.5)

    def drive_vehicle(self,direction,speed):
        channel_main = None
        channel_null = None
        if direction == 'f':
            channel_main = self._drive_fwd_pwm_channel
            channel_null = self._drive_rvr_pwm_channel
        else:
            channel_main = self._drive_rvr_pwm_channel
            channel_null = self._drive_fwd_pwm_channel

        channel_null.ChangeDutyCycle(0)
        channel_main.ChangeDutyCycle(speed)



    def stop_vehicle(self):
        self._drive_fwd_pwm_channel.ChangeDutyCycle(0)
        self._drive_rvr_pwm_channel.ChangeDutyCycle(0)

    def kill_motor(self):
        self._drive_fwd_pwm_channel.stop()
        self._drive_rvr_pwm_channel.stop()
        GPIO.cleanup()

    @property 
    def frequency(self):
        return self._frequency
    
    @frequency.setter 
    def frequency(self,val):
        self._frequency = val
        self.drive_fwd_pwm_channel.ChangeFrequency(val)
        self._drive_rvr_pwm_channel.ChangeFrequency(val)
        return self._frequency

    @property
    def cur_dutyCycle(self):
        return self._cur_dutyCycle

    @property
    def min_dutyCycle(self):
        return self._min_dutyCycle

    @property
    def max_dutyCycle(self):
        return self._max_dutyCycle
    
    @property
    def drive_fwd_pin(self):
        return self._drive_fwd_pin

    @drive_fwd_pin.setter
    def drive_fwd_pin(self,val):
        pos_pwm_pins = [2,5,7,8,10,11,12,13,15,16,18,19,21,22,24,26,29,31,32,33,35,36,37,38,40]
        if (str(pos_pwm_pins).find(", "+str(val)) != -1 or str(pos_pwm_pins).find(str(val)+".") != -1):
            self.drive_fwd_pin.stop()
            self.drive_fwd_pin = val
            GPIO.setup(self.drive_fwd_pin,GPIO.OUT)
            self.drive_fwd_pwm_channel = GPIO.PWM(self.drive_fwd_pin,self.frequency)
            self.drive_fwd_pwm_channel.start(0)
            sleep(.5)
            self.drive_fwd_pwm_channel.start((self.cur_dutyCycle)*100)
            sleep(1)
            return self.drive_fwd_pin
        else:
            print("Sorry, but the desired servo pin provided was an invalid option.")
            print("The following pins can be used for servo assignment:\n" +str(pos_pwm_pins))
            return self._drive_fwd_pin

    @property
    def drive_rvr_pin(self):
        return self._drive_rvr_pin

    @drive_rvr_pin.setter
    def drive_rvr_pin(self,val):
        pos_pwm_pins = [2,5,7,8,10,11,12,13,15,16,18,19,21,22,24,26,29,31,32,33,35,36,37,38,40]
        if (str(pos_pwm_pins).find(", "+str(val)) != -1 or str(pos_pwm_pins).find(str(val)+".") != -1):
            self.drive_rvr_pin.stop()
            self.drive_rvr_pin = val
            GPIO.setup(self.drive_rvr_pin,GPIO.OUT)
            self.drive_rvr_pwm_channel = GPIO.PWM(self.drive_rvr_pin,self.frequency)
            self.drive_rvr_pwm_channel.start(0)
            sleep(.5)
            self.drive_rvr_pwm_channel.start((self.cur_dutyCycle)*100)
            sleep(1)
            return self.drive_rvr_pin
        else:
            print("Sorry, but the desired servo pin provided was an invalid option.")
            print("The following pins can be used for servo assignment:\n" +str(pos_pwm_pins))
            return self._drive_rvr_pin


##~ For property setter methods to work, the class must inherent the 'object' class
class servo(object):

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self._frequency = 60
        self._max_angle = 210                                       ##~Full right position/angle
        self._min_angle = 0                                         ##~Full left position/angle
        self._cur_angle = (self._max_angle-self._min_angle)/2       ##~The center position will be the default position/angle
        self._min_dutyCycle = 2
        self._max_dutyCycle = 18
        self._cur_dutyCycle = (self._max_dutyCycle-self._min_dutyCycle)/2
        self._cur_dutyCycle = self._max_dutyCycle
        self._pwm_pin = 12
        self._slope_offset = 2
        
        GPIO.setup(self._pwm_pin,GPIO.OUT)
        self._pwm_channel = GPIO.PWM(self._pwm_pin,self._frequency)
        self._pwm_channel.start(0)
        sleep(.5)
        #self._pwm_channel.ChangeDutyCycle((self._cur_dutyCycle)*100)                            ##~Centers servo on start
        #sleep(.5) 
        #self._pwm_channel.ChangeDutyCycle(0)
        self._slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self.max_angle,self.min_angle)
        print("Servo_Created with slope: " +str(self._slope))

    def calculate_slope(self,y2,y1,x2,x1):
        slope = (y2-y1)/(x2-x1)
        return slope

    def steer(self,des_pos):
        if (des_pos <= self.max_angle and des_pos >= self.min_angle):
            des_pos = float(des_pos)
            req_dutyCycle = (2+(des_pos/self._max_dutyCycle))
            self._pwm_channel.ChangeDutyCycle(req_dutyCycle)
            sleep(1)
            self._pwm_channel.ChangeDutyCycle(0)
        
            print("Moving servo to position: " +str(int(des_pos)))
            print("Duty Cycle was set to: " +str(req_dutyCycle))
        else:
            print("The desired servo position/angle is not a valid value.")
            print("Please try again with an integer  value within the following range: " +str(self.min_angle) +"-" +str(self.max_angle))

    def kill_servo(self):
        self.pwm_channel.stop()

    #getting the value
    @property
    def max_angle(self):
        return self._max_angle
    
    @max_angle.setter
    def max_angle(self,val):
        self._max_angle = val
        self._slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self._max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._max_angle
    
    @property
    def min_angle(self):
        return self._min_angle
    
    @min_angle.setter
    def min_angle(self,val):
        self._min_angle = val
        self._slope = self.calculate_slope(self.max_dutyCycle,self.min_dutyCycle,self.max_angle,self._min_angle)
        print("new slope : " +str(self.slope))
        return self._min_angle
    
    @property
    def max_dutyCycle(self):
        return self._max_dutyCycle
    
    @max_dutyCycle.setter
    def max_dutyCycle(self,val):
        self._max_dutyCycle = val
        self._slope = self.calculate_slope(self._max_dutyCycle,self.min_dutyCycle,self.max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._max_dutyCycle
    
    @property
    def min_dutyCycle(self):
        return self._min_dutyCycle
    
    @min_dutyCycle.setter
    def min_dutyCycle(self,val):
        self._max_dutyCycle = val
        self._slope = self.calculate_slope(self.max_dutyCycle,self._min_dutyCycle,self.max_angle,self.min_angle)
        print("new slope : " +str(self.slope))
        return self._min_dutyCycle
       
    @property
    def pwm_pin(self):
        return self._pwm_pin
    
    @pwm_pin.setter
    def pwm_pin(self,val):
        pos_pwm_pins = [2,5,7,8,10,11,12,13,15,16,18,19,21,22,24,26,29,31,32,33,35,36,37,38,40]
        if (str(pos_pwm_pins).find(", "+str(val)) != -1 or str(pos_pwm_pins).find(str(val)+".") != -1):
            self.pwm_channel.stop()
            self._pwm_pin = val
            GPIO.setup(self._pwm_pin,GPIO.OUT)
            self.pwm_channel = GPIO.PWM(self._pwm_pin,self.frequency)
            self.pwm_channel.start(0)
            sleep(.5)
            self.pwm_channel.start((self.cur_dutyCycle)*100)
            sleep(1)
            return self._pwm_pin
        else:
            print("Sorry, but the desired servo pin provided was an invalid option.")
            print("The following pins can be used for servo assignment:\n" +str(pos_pwm_pins))
            return self._pwm_pin
    
    @property
    def pwm_channel(self):
        return self._pwm_channel
    
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
        if (val >= self.min_angle and val <= self.max_angle):
            self.steer(val)
            self._cur_angle = val
            return self._cur_angle 
        else:
            self.steer(val)
            return self._cur_angle 
    
    @property
    def cur_dutyCycle(self):
        return self._cur_dutyCycle

    @property
    def slope(self):
        return self._slope


