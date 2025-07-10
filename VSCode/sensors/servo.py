# Red (VCC)	5V (Pin 2 or 4) ✅ (short test only)
# Brown/Black (GND)	GND (Pin 6)
# Yellow/Orange (Signal)	GPIO 17 (Pin 11)

from gpiozero import Servo
from time import sleep

servo = Servo(17)  # GPIO 17

print("Center")
servo.mid()
sleep(1)

print("Right")
servo.max()
sleep(1)

print("Left")
servo.min()
sleep(1)

print("Back to center")
servo.mid()
sleep(1)
