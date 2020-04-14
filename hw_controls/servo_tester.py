from servo_ctrl import servo

s = servo()
print(vars(s))
print("max_angle: " +str(s.max_angle))
print("slope: " +str(s.slope))
for i in range(0,3):
    s.steer(360)
    print("turning left")

for i in range(0,6):
    s.steer(0)
    print("turning right")
for i in range(0,3):
    s.steer(360)
    print("Return to center")

s.kill_servo()
