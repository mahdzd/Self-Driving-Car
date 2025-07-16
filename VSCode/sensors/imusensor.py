# 	MPU6050 wired via I2C	SDA = GPIO 2 (Pin 3), SCL = GPIO 3 (Pin 5)
#	VCC to 3.3V or 5V	Many modules work on 3.3V or 5V
#	Detected at I2C address 0x68	Use i2cdetect -y 1 to confirm
#	Python module mpu6050 installed	Installed via pip in venv or system

from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)  # I2C address

while True:
    accel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()

    print(f"Accel: x={accel['x']:.2f}, y={accel['y']:.2f}, z={accel['z']:.2f}")
    print(f"Gyro:  x={gyro['x']:.2f}, y={gyro['y']:.2f}, z={gyro['z']:.2f}")
    print("-----------")
    time.sleep(0.5)
