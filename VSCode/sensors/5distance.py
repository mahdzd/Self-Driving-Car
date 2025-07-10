import time
import board
import busio
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# I2C setup
i2c = busio.I2C(board.SCL, board.SDA)

# GPIO pins for XSHUT — only 4 sensors now
XSHUT_PINS = [17, 27, 22, 23]  # Use any 4 GPIO pins you like
NEW_ADDRESSES = [0x30, 0x31, 0x32, 0x33]  # Unique addresses for each

# Setup GPIO
GPIO.setmode(GPIO.BCM)
for pin in XSHUT_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)  # Disable all sensors

time.sleep(0.1)

# Power on each sensor one by one and assign new I2C address
sensors = []
for i, pin in enumerate(XSHUT_PINS):
    GPIO.output(pin, GPIO.HIGH)     # Enable this sensor
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
