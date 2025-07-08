from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# Use GPIO 18 (hardware PWM)
factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory)

while True:
    servo.mid()   # center
    sleep(1)
    servo.min()   # left
    sleep(1)
    servo.max()   # right
    sleep(1)
