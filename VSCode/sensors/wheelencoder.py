from gpiozero import Button
from time import time

class WheelEncoder:
    def __init__(self, pin_left=17, pin_right=27, pulses_per_rev=20, wheel_circ_cm=21.0):
        self.PULSES_PER_REV = pulses_per_rev
        self.WHEEL_CIRCUMFERENCE = wheel_circ_cm

        self.left_count = 0
        self.right_count = 0
        self.left_last_time = time()
        self.right_last_time = time()
        self.left_total_distance = 0.0
        self.right_total_distance = 0.0

        self.left_sensor = Button(pin_left, pull_up=True)
        self.right_sensor = Button(pin_right, pull_up=True)

        self.left_sensor.when_pressed = self.left_pulse
        self.right_sensor.when_pressed = self.right_pulse

    def left_pulse(self):
        self.left_count += 1
        self.left_total_distance += self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV
        self.left_last_time = time()

    def right_pulse(self):
        self.right_count += 1
        self.right_total_distance += self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV
        self.right_last_time = time()

    def get_speeds(self):
        now = time()
        left_dt = now - self.left_last_time
        right_dt = now - self.right_last_time

        left_speed = (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV) / left_dt if left_dt < 1 else 0
        right_speed = (self.WHEEL_CIRCUMFERENCE / self.PULSES_PER_REV) / right_dt if right_dt < 1 else 0

        return left_speed, right_speed

    def get_distances(self):
        return self.left_total_distance, self.right_total_distance
