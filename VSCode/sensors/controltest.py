from time import sleep
from gpiozero import Device
from gpiozero.pins.native import NativeFactory
Device.pin_factory = NativeFactory()

from CarController import CarController

car = CarController(in1_pin=14, in2_pin=15, ena_pin=21, servo_pin=12)

try:
    while True:
        user_input = input("Enter: direction f/b, speed [0-1], angle [-30 to 30] (e.g. f 0.6 -15): ")
        parts = user_input.strip().split()
        if len(parts) != 3:
            print("Invalid format.")
            continue

        direction, speed, angle = parts
        speed = float(speed)
        angle = float(angle)

        car.setAll(direction, speed, angle)
        sleep(1)
        car.stop()

except KeyboardInterrupt:
    print("Stopped.")

finally:
    car.stop()
