from gpiozero import Motor, AngularServo
from time import sleep

class CarController:
    def __init__(self, motor_forward_pin, motor_backward_pin, servo_pin):
        # Initialize motor (L298N style)
        self.motor = Motor(forward=motor_forward_pin, backward=motor_backward_pin)

        # Initialize servo (range may need tuning for your specific servo)
        self.servo = AngularServo(
            servo_pin,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

    def set_motor(self, direction, speed=1.0):
        """
        direction: 'forward', 'backward', or 'stop'
        speed: float between 0.0 and 1.0
        """
        if direction == 'forward':
            self.motor.forward(speed)
        elif direction == 'backward':
            self.motor.backward(speed)
        else:
            self.motor.stop()

    def set_steering(self, angle):
        """
        Directly set the servo angle.
        angle: degrees (between 0 and 180)
        """
        angle = max(0, min(180, angle))  # Clamp
        self.servo.angle = angle
        sleep(0.1)

    def stop(self):
        self.motor.stop()

# === Demo usage ===
if __name__ == "__main__":
    try:
        # Define your pin numbers here
        car = CarController(motor_forward_pin=17, motor_backward_pin=18, servo_pin=22)

        print("Centering steering and moving forward")
        car.set_steering(90)
        car.set_motor('forward', 0.7)
        sleep(2)

        print("Turning left")
        car.set_steering(45)
        sleep(1)

        print("Turning right")
        car.set_steering(135)
        sleep(1)

        car.stop()

    except KeyboardInterrupt:
        print("Interrupted")

    finally:
        car.stop()
