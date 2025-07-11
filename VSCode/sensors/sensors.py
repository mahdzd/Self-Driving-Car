from alldistance import DistanceSensor
from colorsensor import read_frequency
from imusensor import sensor as imu_sensor
from steeringencoder import steps_to_angle, encoder as steering_encoder
from wheelencoder import left_total_distance, right_total_distance, left_count, right_count
from wheelencoder import left_sensor, right_sensor

import time

# do this in main:
# sensors = Sensors()
# if not sensors.ready:
#     print("Sensors setup failed. Handle fallback or retry.")
# else:
#     data = sensors.read_all()


class Sensors:
    def __init__(self):
        self.ready = True  # assume ready unless a failure happens

        try:
            # Distance sensors
            self.dist_sensors = []
            self.dist_sensors_pins = [17, 20, 22, 23]
            self.dist_sensors_addresses = [0x29, 0x30, 0x31, 0x32]
            for i in range(4):
                s = DistanceSensor(self.dist_sensors_pins[i])
                s.change_address(self.dist_sensors_addresses[i])
                self.dist_sensors.append(s)
        except Exception as e:
            print(f"[ERROR] Distance sensor init failed: {e}")
            self.ready = False

        try:
            self.color_sensor_ready = True  # color sensor is auto-initialized in module
            _ = read_frequency(False, False)  # dummy read to test
        except Exception as e:
            print(f"[ERROR] Color sensor init failed: {e}")
            self.ready = False

        try:
            _ = imu_sensor.get_accel_data()
            _ = imu_sensor.get_gyro_data()
        except Exception as e:
            print(f"[ERROR] IMU sensor init failed: {e}")
            self.ready = False

        try:
            _ = steps_to_angle(steering_encoder.steps)
        except Exception as e:
            print(f"[ERROR] Steering encoder init failed: {e}")
            self.ready = False

        try:
            _ = left_total_distance
            _ = right_total_distance
        except Exception as e:
            print(f"[ERROR] Wheel encoder init failed: {e}")
            self.ready = False

    def read_distances(self):
        return [sensor.read() for sensor in self.dist_sensors]

    def read_color(self):
        red = read_frequency(False, False)
        green = read_frequency(True, True)
        blue = read_frequency(False, True)
        return [red, green, blue]

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
