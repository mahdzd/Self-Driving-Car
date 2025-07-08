import board
import busio
import time
import adafruit_vl53l0x
import RPi.GPIO as GPIO

# Use GPIO 8 (Pin 24) to control XSHUT
XSHUT_PIN = 8
GPIO.setmode(GPIO.BCM)
GPIO.setup(XSHUT_PIN, GPIO.OUT)
GPIO.output(XSHUT_PIN, GPIO.HIGH)  # Enable sensor

# Set up I2C
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_vl53l0x.VL53L0X(i2c)

try:
    while True:
        distance = sensor.range
        print(f"Distance: {distance} mm")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
