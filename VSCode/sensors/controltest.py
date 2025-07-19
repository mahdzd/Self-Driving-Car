from time import sleep

from allEncodersClass import RobotEncoders
from CarController import CarController

car = CarController(in1_pin=14, in2_pin=15, ena_pin=13, servo_pin=12)
encoders = RobotEncoders()
try:
    while True:
        user_input = input("Enter: direction f/b, speed [0-1], angle [-30 to 30] (e.g. f 0.6 -15): ")
        parts = user_input.strip().split()  
        if len(parts) != 4:
            print("Invalid format.")
            continue

        direction, speed, angle, t1 = parts
        speed = float(speed)
        angle = float(angle)

        car.setAll(direction, speed, angle)
        sleep(float(t1))
        car.brake(encoders)
        car.stop()
        

except KeyboardInterrupt:
    print("Stopped.")

finally:
    car.stop()
