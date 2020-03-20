from servo_ctrl import servo

s = servo()
print(vars(s))
print("max_angle: " +str(s.max_angle))
print("slope: " +str(s.slope))
s.max_angle = 180