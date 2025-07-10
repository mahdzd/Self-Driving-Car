# VL53L0X is powered
# XSHUT is tied to 3.3V (Pin 1)
# SDA and SCL are connected to GPIO 2 & 3
# source ~/wro-env/bin/activate if using venv

import smbus2
import time
<<<<<<< HEAD
import adafruit_vl53l0x
from gpiozero import DigitalOutputDevice

# XSHUT connected to GPIO 17 (Pin 11)
XSHUT_PIN = 17
xshut = DigitalOutputDevice(XSHUT_PIN)
xshut.on()
time.sleep(0.1)  # Give sensor time to power up
=======

ADDR = 0x29
bus = smbus2.SMBus(1)
>>>>>>> ebf2f9c6eba717eb4081e8896e5de33dfc72e46d

SYSRANGE_START = 0x00
RESULT_RANGE_STATUS = 0x14
SYSTEM_INTERRUPT_CLEAR = 0x0B

def read_distance():
    # Start a single measurement
    bus.write_byte_data(ADDR, SYSRANGE_START, 0x01)
    time.sleep(0.05)

    # Read result
    data = bus.read_i2c_block_data(ADDR, RESULT_RANGE_STATUS + 10, 2)
    distance = (data[0] << 8) + data[1]

    # Clear interrupt
    bus.write_byte_data(ADDR, SYSTEM_INTERRUPT_CLEAR, 0x01)

    return distance

try:
    while True:
        dist = read_distance()
        print(f"Distance: {dist} mm")
        time.sleep(0.2)

except KeyboardInterrupt:
<<<<<<< HEAD
    print("Stopped.")
=======
    print("Stopped")

