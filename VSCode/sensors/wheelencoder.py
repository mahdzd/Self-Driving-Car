from gpiozero import Button
from time import time, sleep

class WheelEncoder:
    def __init__(self, pin_left=27, pin_right=19, pulses_per_rev=20, wheel_circ_cm=20.41):
        self.PULSES_PER_REV = pulses_per_rev
        self.WHEEL_CIRCUMFERENCE = wheel_circ_cm

        # Pulse counters
        self.left_count = 0
        self.right_count = 0

        # Timing
        self.left_last_time = time()
        self.right_last_time = time()

        # Distance tracking
        self.left_total_distance = 0.0
        self.right_total_distance = 0.0

        # Direction multipliers (+1 forward, -1 backward)
        self.left_direction = 1
        self.right_direction = 1

        # GPIO setup
        self.left_sensor = Button(pin_left, pull_up=True)
        self.right_sensor = Button(pin_right, pull_up=True)

        # Attach callbacks
        self.left_sensor.when_pressed = self.left_pulse
        self.right_sensor.when_pressed = self.right_pulse

    def set_directions(self, left_dir: int, right_dir: int):
        """Set direction of wheels: 1 for forward, -1 for backward."""
        self.left_direction = 1 if left_dir >= 0 else -1
        self.right_direction = 1 if right_dir >= 0 else -1

    def left_pulse(self):
        self.left_count += 1
        self.left_total_distance += self.left_direction * (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV)
        self.left_last_time = time()

    def right_pulse(self):
        self.right_count += 1
        self.right_total_distance += self.right_direction * (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV)
        self.right_last_time = time()

    def get_speeds(self):
        now = time()
        left_dt = now - self.left_last_time
        right_dt = now - self.right_last_time

        left_speed = (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV) / left_dt if left_dt < 1 else 0
        right_speed = (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV) / right_dt if right_dt < 1 else 0

        return self.left_direction * left_speed, self.right_direction * right_speed

    def get_distances(self):
        return self.left_total_distance, self.right_total_distance

if __name__ == "__main__":
    encoder = WheelEncoder()

    try:
        # Set direction: 1 for forward, -1 for reverse
        encoder.set_directions(left_dir=1, right_dir=1)

        print("Monitoring wheel encoders... Press Ctrl+C to stop.\n")
        while True:
            left_speed, right_speed = encoder.get_speeds()
            left_dist, right_dist = encoder.get_distances()

            print(f"Left Speed: {left_speed:.2f} cm/s | Right Speed: {right_speed:.2f} cm/s")
            print(f"Left Distance: {left_dist:.2f} cm | Right Distance: {right_dist:.2f} cm\n")

            sleep(1)

    except KeyboardInterrupt:
        print("\nStopped by user.")
