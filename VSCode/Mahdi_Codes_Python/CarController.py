from gpiozero import PWMOutputDevice, DigitalOutputDevice, AngularServo
from time import sleep

class CarController:
    def __init__(self, in1_pin, in2_pin, ena_pin, servo_pin):
        # Motor control pins
        self.in1 = DigitalOutputDevice(in1_pin)
        self.in2 = DigitalOutputDevice(in2_pin)
        self.ena = PWMOutputDevice(ena_pin)

        # Steering servo (adjust angles and pulse widths if needed)
        self.servo = AngularServo(
            servo_pin,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

    def set_motor(self, direction, speed=1.0):
        speed = max(0.0, min(1.0, speed))
        if direction == 'forward':
            self.in1.on()
            self.in2.off()
            self.ena.value = speed
        elif direction == 'backward':
            self.in1.off()
            self.in2.on()
            self.ena.value = speed
        else:
            self.stop()

    def set_steering(self, angle):
        angle = max(0, min(180, angle))
        self.servo.angle = angle
        print(f"Steering set to {angle} degrees")
        sleep(0.1)

    def stop(self):
        self.in1.off()
        self.in2.off()
        self.ena.value = 0.0

# === Demo usage ===
if __name__ == "__main__":
    try:
        car = CarController(in1_pin=17, in2_pin=18, ena_pin=4, servo_pin=4)

        print("Centering steering")
        car.set_steering(90)
        sleep(2)

        # print("Ramping up motor speed from 0.0 to 0.5")
        # for i in range(0, 11):
            # speed = i * 0.05
            # car.set_motor('forward', speed)
            # print(f"Speed set to {speed:.2f}")
            # sleep(0.5)

        # print("Turning left")
        # car.set_steering(45)
        # sleep(1)

        # print("Turning right")
        # car.set_steering(135)
        # sleep(1)

        # print("Stopping")
        # car.stop()

    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        car.stop()
