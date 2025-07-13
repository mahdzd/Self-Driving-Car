from gpiozero import AngularServo
from time import sleep

# Initialize the servo on GPIO pin 17 with angle range
servo = AngularServo(4, min_angle=0, max_angle=360)

servo.angle = 230
sleep(1)
print(servo.is_active)
print(servo.value)

servo.detach()
servo.close()



