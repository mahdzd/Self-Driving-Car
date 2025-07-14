#this one works!!
from gpiozero import PWMOutputDevice, DigitalOutputDevice
from time import sleep
from servoClass import myServo
import keyboard

class CarController:
    def __init__(self, in1_pin, in2_pin, ena_pin, servo_pin):
        # Motor control pins
        self.in1 = DigitalOutputDevice(in1_pin)
        self.in2 = DigitalOutputDevice(in2_pin)
        self.ena = PWMOutputDevice(ena_pin)

        # Steering servo (adjust angles and pulse widths if needed)
        self.servo = myServo(servo_pin, center_angle=90, max_deviation=30)

    def set_motor(self, direction, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        if direction == 'f':
            self.in1.on()
            self.in2.off()
            self.ena.value = speed
        elif direction == 'b':
            self.in1.off()
            self.in2.on()
            self.ena.value = speed
        else:
            self.stop()

    def set_steering(self, angle):
        self.servo.set_servo_angle(angle)
        print(f"Steering set to {angle} degrees")
        sleep(0.05)

    def stop(self):

        self.in1.off()
        self.in2.off()
        self.ena.value = 0.0

    def setAll(self,direction,speed,angle):
        self.set_motor(direction,speed)
        self.set_steering(angle)

        
# === Demo usage ===
if __name__ == "__main__":
    try:
        car = CarController(in1_pin=14, in2_pin=15, ena_pin=21, servo_pin=17)

        print("\nControl car using keys:")
        print("  w = forward")
        print("  s = backward")
        print("  a = steer left")
        print("  d = steer right")
        print("  space = stop")
        print("  q = quit")
        
        steering = 0

        while True:
            if keyboard.is_pressed('q'):
                break
            elif keyboard.is_pressed('w'):
                car.set_motor('f', 0.9)
            elif keyboard.is_pressed('s'):
                car.set_motor('b', 0.9    )
            elif keyboard.is_pressed(' '):
                car.stop()
            elif keyboard.is_pressed('a'):
                steering = max(-30, steering - 5)
                car.set_steering(steering)
                sleep(0.2)
            elif keyboard.is_pressed('d'):
                steering = min(30, steering + 5)
                car.set_steering(steering)
                sleep(0.2)

            sleep(0.01)

        car.stop()

    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        car.stop()
