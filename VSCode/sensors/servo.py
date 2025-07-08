from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory)  # GPIO 18 = Pin 12

while True:
    print("Center")
    servo.mid()
    sleep(1)

    print("Left")
    servo.min()
    sleep(1)

    print("Right")
    servo.max()
    sleep(1)
