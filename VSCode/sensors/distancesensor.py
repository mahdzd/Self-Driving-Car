import board
import busio
import time
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# XSHUT connected to GPIO 17 (Pin 11)
XSHUT_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(XSHUT_PIN, GPIO.OUT)
GPIO.output(XSHUT_PIN, GPIO.HIGH)  # Turn on sensor

# Setup I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize VL53L0X
print("Initializing sensor...")
sensor = adafruit_vl53l0x.VL53L0X(i2c)

# Read distances
try:
    while True:
        distance = sensor.range
        print(f"Distance: {distance} mm")
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stopped.")
import board
import busio
import time
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# XSHUT connected to GPIO 17 (Pin 11)
XSHUT_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(XSHUT_PIN, GPIO.OUT)
GPIO.output(XSHUT_PIN, GPIO.HIGH)  # Turn on sensor

# Setup I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize VL53L0X
print("Initializing sensor...")
sensor = adafruit_vl53l0x.VL53L0X(i2c)

# Read distances
try:
    while True:
        distance = sensor.range
        print(f"Distance: {distance} mm")
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Stopped.")
