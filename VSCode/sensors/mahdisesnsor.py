
from alldistance import DistanceSensor
from colorsensor import read_frequency, detect_main_color
from imusensor import sensor as imu_sensor
import time
from mpu6050 import mpu6050

dist_sensors=[] 
dist_sensors_pins=[4, 18, 25, 12] #GPIo numbering
dist_sensors_Addresses=[0x30,0x31,0x32,0x33,]  # I2C addresses
for i in range(4):
    try:
        dist_sensors.append(DistanceSensor(dist_sensors_pins[i]))#create a sensor object and intlize it and add it to the array
        dist_sensors[i].change_address(dist_sensors_Addresses[i])#give each sensor a costum address
    except Exception as e:
        print(e)

imusen = mpu6050(0x68)
_ = read_frequency(False, False)

while True:
	try:
		for i in range(4):
			print("reading from sensor ",i)
			print(dist_sensors[i].read())
			time.sleep(0.3)
			
		   
		accel = imusen.get_accel_data()
		gyro = imusen.get_gyro_data()
		print(f"Accel: x={accel['x']:.2f}, y={accel['y']:.2f}, z={accel['z']:.2f}")
		print(f"Gyro:  x={gyro['x']:.2f}, y={gyro['y']:.2f}, z={gyro['z']:.2f}")
		print("-----------")
		time.sleep(0.5)
		
		print(detect_main_color())
		time.sleep(0.5)
	except KeyboardInterrupt:
		break
