from car_ctrl import servo
import time
#max angle turns right
#0 turns left
def test_servo_rotation():
    s = servo()
    print(vars(s))
    print("max_angle: " +str(s.max_angle))
    print("slope: " +str(s.slope))
    for i in range(0,2):
        s.steer(s.max_angle)
        print("turning left")
        time.sleep(0.5)

    for i in range(0,3):
        s.steer(0)
        time.sleep(0.5)
        print("turning right")
    
    for i in range(0,1):
        s.steer(s.max_angle)
        time.sleep(0.5)
        print("Return to center")

    s.kill_servo()

#test_servo_rotation()
