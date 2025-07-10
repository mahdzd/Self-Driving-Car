import time
import board
import busio
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# GPIO pins for XSHUT
XSHUT_PINS = [17, 27, 22, 23, 24]
NEW_ADDRESSES = [0x30, 0x31, 0x32, 0x33, 0x34]

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in XSHUT_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

time.sleep(0.1)

# Power on sensors one by one and assign new addresses
sensors = []
for i, pin in enumerate(XSHUT_PINS):
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.1)

    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    sensor.set_address(NEW_ADDRESSES[i])
    sensors.append(sensor)

# Read from all sensors
try:
    while True:
        for i, sensor in enumerate(sensors):
            dist = sensor.range
            print(f"Sensor {i+1}: {dist} mm")
        print("------")
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Stopped")

finally:
    GPIO.cleanup()
