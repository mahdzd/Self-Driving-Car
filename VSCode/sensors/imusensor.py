from mpu6050 import mpu6050
import time

sensor = mpu6050(0x68)  # Default I2C address

while True:
    accel = sensor.get_accel_data()
    gyro = sensor.get_gyro_data()
    
    print("Accelerometer:")
    print(f"  X: {accel['x']:.2f}g  Y: {accel['y']:.2f}g  Z: {accel['z']:.2f}g")
    
    print("Gyroscope:")
    print(f"  X: {gyro['x']:.2f}°/s  Y: {gyro['y']:.2f}°/s  Z: {gyro['z']:.2f}°/s")
    
    print("—" * 30)
    time.sleep(0.5)
