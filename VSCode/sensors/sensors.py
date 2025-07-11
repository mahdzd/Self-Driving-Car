from 4distance import DistanceSensor
from colorsensor import detect_main_color
def read_color(self):
    return detect_main_color()

from imusensor import sensor as imu_sensor
from steeringencoder import steps_to_angle, encoder as steering_encoder
from wheelencoder import left_total_distance, right_total_distance, left_count, right_count
from wheelencoder import left_sensor, right_sensor

import time

class Sensors:
    def __init__(self):
        self.ready_distance = False
        self.ready_color = False
        self.ready_imu = False
        self.ready_steering = False
        self.ready_wheel = False

        try:
            self.dist_sensors = []
            self.dist_sensors_pins = [17, 20, 22, 23]
            self.dist_sensors_addresses = [0x29, 0x30, 0x31, 0x32]
            for i in range(4):
                s = DistanceSensor(self.dist_sensors_pins[i])
                s.change_address(self.dist_sensors_addresses[i])
                self.dist_sensors.append(s)
            self.ready_distance = True
        except Exception as e:
            print(f"[ERROR] Distance sensors init failed: {e}")

        try:
            _ = read_frequency(False, False)
            self.ready_color = True
        except Exception as e:
            print(f"[ERROR] Color sensor init failed: {e}")

        try:
            _ = imu_sensor.get_accel_data()
            _ = imu_sensor.get_gyro_data()
            self.ready_imu = True
        except Exception as e:
            print(f"[ERROR] IMU sensor init failed: {e}")

        try:
            _ = steps_to_angle(steering_encoder.steps)
            self.ready_steering = True
        except Exception as e:
            print(f"[ERROR] Steering encoder init failed: {e}")

        try:
            _ = left_total_distance
            _ = right_total_distance
            _ = left_count
            _ = right_count
            self.ready_wheel = True
        except Exception as e:
            print(f"[ERROR] Wheel encoder init failed: {e}")

        self.ready = all([
            self.ready_distance,
            self.ready_color,
            self.ready_imu,
            self.ready_steering,
            self.ready_wheel
        ])

    def read_distances(self):
        return [sensor.read() for sensor in self.dist_sensors]
 
    def read_color(self):
    
     return detect_main_color()


    def read_imu(self):
        accel = imu_sensor.get_accel_data()
        gyro = imu_sensor.get_gyro_data()
        return [accel, gyro]

    def read_steering_angle(self):
        return steps_to_angle(steering_encoder.steps)

    def read_wheel_encoders(self):
        return {
            "left_distance": left_total_distance,
            "right_distance": right_total_distance,
            "left_pulses": left_count,
            "right_pulses": right_count
        }

    def read_all(self):
        return [
            self.read_distances(),
            self.read_color(),
            self.read_imu(),
            self.read_steering_angle(),
            self.read_wheel_encoders()
        ]
