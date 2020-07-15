from time import sleep
from .car_ctrl import driver

def test_motor_speed_and_direction():
    d = driver()
    for speed in range(20,80,10):
        d.drive_vehicle('f',speed)
        print("Running motor forward @ " +str(speed) +"% speed.")
        sleep(3)

    d.stop_vehicle()
    sleep(1)
    for speed in range(20,80,10):
        d.drive_vehicle('r',speed)
        print("Running motor in reverse @ " +str(speed) +"% speed." )
        sleep(3)

    d.stop_vehicle()
    d.kill_motor()

#test_motor_speed_and_direction()
