import time
import board
import busio
import adafruit_vl53l0x
from gpiozero import DigitalOutputDevice

# I2C setup (SCL = GPIO3, SDA = GPIO2 by default on Pi)
i2c = busio.I2C(board.SCL, board.SDA)

# Define XSHUT pins using gpiozero DigitalOutputDevice
xshut_pins = [17, 27, 22, 23]  # BCM numbering
xshuts = [DigitalOutputDevice(pin) for pin in xshut_pins]

# New unique I2C addresses
new_addresses = [0x30, 0x31, 0x32, 0x33]

# Disable all sensors initially
for x in xshuts:
    x.off()

time.sleep(0.1)

# Enable each sensor one by one and set unique I2C address
sensors = []
for i, x in enumerate(xshuts):
    x.on()
    time.sleep(0.1)  # Let it boot

    sensor = adafruit_vl53l0x.VL53L0X(i2c)
    sensor.set_address(new_addresses[i])
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
