from gpiozero import Button
from mpu6050 import mpu6050
from time import time, sleep

class RobotEncoders:
    def __init__(self,
                 wheel_left_pin=27, wheel_right_pin=19,
                 pulses_per_rev=20, wheel_circ_cm=21.0):
        
        self.PULSES_PER_REV = pulses_per_rev
        self.WHEEL_CIRC = wheel_circ_cm

        self.left_count = 0
        self.right_count = 0
        self.left_last_time = time()
        self.right_last_time = time()
        self.left_total_distance = 0.0
        self.right_total_distance = 0.0

        self.left_sensor = Button(wheel_left_pin, pull_up=True)
        self.right_sensor = Button(wheel_right_pin, pull_up=True)
        self.left_sensor.when_pressed = self._left_pulse
        self.right_sensor.when_pressed = self._right_pulse

        self.imu = mpu6050(0x68)  # MPU-6050 I2C

    def _left_pulse(self):
        self.left_count += 1
        self.left_total_distance += self.WHEEL_CIRC / self.PULSES_PER_REV
        self.left_last_time = time()

    def _right_pulse(self):
        self.right_count += 1
        self.right_total_distance += self.WHEEL_CIRC / self.PULSES_PER_REV
        self.right_last_time = time()

    def get_linear_speeds(self):
        now = time()
        dt_l = now - self.left_last_time
        dt_r = now - self.right_last_time

        v_l = (self.WHEEL_CIRC / self.PULSES_PER_REV) / dt_l if dt_l < 1 else 0
        v_r = (self.WHEEL_CIRC / self.PULSES_PER_REV) / dt_r if dt_r < 1 else 0
        return v_l, v_r  # cm/s

    def get_angular_speeds(self):
        now = time()
        dt_l = now - self.left_last_time
        dt_r = now - self.right_last_time

        rev_l = 1 / self.PULSES_PER_REV / dt_l if dt_l < 1 else 0
        rev_r = 1 / self.PULSES_PER_REV / dt_r if dt_r < 1 else 0

        omega_l = 2 * 3.1416 * rev_l  # rad/s
        omega_r = 2 * 3.1416 * rev_r
        return omega_l, omega_r

    def get_distances(self):
        return self.left_total_distance, self.right_total_distance  # cm

    def reset_wheels(self):
        self.left_count = 0
        self.right_count = 0
        self.left_total_distance = 0
        self.right_total_distance = 0
        self.left_last_time = time()
        self.right_last_time = time()

    def reset_all(self):
        self.reset_wheels()

    def get_yaw_rate(self):
        gyro = self.imu.get_gyro_data()
        return gyro['z']  # deg/sec

    def get_motion_state(self):
        v_l, v_r = self.get_linear_speeds()
        yaw = self.get_yaw_rate()
        return {
            "left_speed": v_l,
            "right_speed": v_r,
            "yaw_rate": yaw
        }
