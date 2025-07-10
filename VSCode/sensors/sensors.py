import time
import smbus2
from gpiozero import DigitalOutputDevice, DigitalInputDevice
from mpu6050 import mpu6050

# ------------ VL53L0X Distance Sensor ------------
class DistanceSensor:
    def __init__(self, i2c_bus=1, address=0x29):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self.SYSRANGE_START = 0x00
        self.RESULT_RANGE_STATUS = 0x14
        self.SYSTEM_INTERRUPT_CLEAR = 0x0B

    def read(self):
        self.bus.write_byte_data(self.address, self.SYSRANGE_START, 0x01)
        time.sleep(0.05)
        data = self.bus.read_i2c_block_data(self.address, self.RESULT_RANGE_STATUS + 10, 2)
        distance = (data[0] << 8) + data[1]
        self.bus.write_byte_data(self.address, self.SYSTEM_INTERRUPT_CLEAR, 0x01)
        return distance

# ------------ TCS3200 Color Sensor ------------
class ColorSensor:
    def __init__(self, s0=17, s1=27, s2=22, s3=23, out_pin=24):
        self.S2 = DigitalOutputDevice(s2)
        self.S3 = DigitalOutputDevice(s3)
        self.OUT = DigitalInputDevice(out_pin)

        # Set frequency scaling to 20%
        self.S0 = DigitalOutputDevice(s0)
        self.S1 = DigitalOutputDevice(s1)
        self.S0.on()
        self.S1.off()

    def read_frequency(self, s2, s3):
        self.S2.value = s2
        self.S3.value = s3
        time.sleep(0.1)
        start = time.time()
        for _ in range(10):
            self.OUT.wait_for_active()
            self.OUT.wait_for_inactive()
        duration = time.time() - start
        return 10 / duration if duration != 0 else 0

    def read(self):
        r = self.read_frequency(False, False)
        g = self.read_frequency(True, True)
        b = self.read_frequency(False, True)
        return {"r": r, "g": g, "b": b}

# ------------ MPU6050 Motion Sensor ------------
class MotionSensor:
    def __init__(self, address=0x68):
        self.sensor = mpu6050(address)

    def read(self):
        accel = self.sensor.get_accel_data()
        gyro = self.sensor.get_gyro_data()
        return {"accel": accel, "gyro": gyro}

# ------------ Sensor Suite (Master Controller) ------------
class SensorSuite:
    def __init__(self):
        self.distance_sensor = DistanceSensor()
        self.color_sensor = ColorSensor()
        self.motion_sensor = MotionSensor()

    def read_all(self):
        distance = self.distance_sensor.read()
        color = self.color_sensor.read()
        motion = self.motion_sensor.read()
        return {
            "distance": distance,
            "color": color,
            "motion": motion
        }

# ------------ Example Test ------------
if __name__ == "__main__":
    sensors = SensorSuite()
    try:
        while True:
            data = sensors.read_all()
            print(f"Distance: {data['distance']} mm")
            print(f"Color: R={data['color']['r']:.1f}, G={data['color']['g']:.1f}, B={data['color']['b']:.1f}")
            accel = data['motion']['accel']
            gyro = data['motion']['gyro']
            print(f"Accel: x={accel['x']:.2f}, y={accel['y']:.2f}, z={accel['z']:.2f}")
            print(f"Gyro:  x={gyro['x']:.2f}, y={gyro['y']:.2f}, z={gyro['z']:.2f}")
            print("---------------")
            time.sleep(1)

    except KeyboardInterrupt:
        print("Stopped")
