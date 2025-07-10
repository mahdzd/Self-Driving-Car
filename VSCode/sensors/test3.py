from smbus2 import SMBus
import time

VL53L0X_DEFAULT_I2C_ADDR = 0x29

def read_distance(bus):
    # VL53L0X has a complex protocol, this is just placeholder
    # You should use Adafruit's library if you need actual ranging
    # Here we just test I2C communication
    try:
        bus.write_quick(VL53L0X_DEFAULT_I2C_ADDR)
        return True
    except Exception as e:
        print("Sensor not responding:", e)
        return False

with SMBus(1) as bus:
    while True:
        if read_distance(bus):
            print("VL53L0X detected.")
        else:
            print("VL53L0X not detected.")
        time.sleep(1)
