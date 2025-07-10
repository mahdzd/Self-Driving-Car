# 🔌 | Color sensor is wired to Pi | Pins: S0=17, S1=27, S2=22, S3=23, OUT=24     |
# ⚡  | VCC connected to **5V**     | (TCS3200 needs 5V, not 3.3V!)                |
# 🔁 | `gpiozero` is installed     | Already installed with Pi OS                 |


from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

# Setup
S0 = DigitalOutputDevice(17)
S1 = DigitalOutputDevice(27)
S2 = DigitalOutputDevice(22)
S3 = DigitalOutputDevice(23)
OUT = DigitalInputDevice(24)

# Set frequency scaling to 20%
S0.on()
S1.off()

def read_frequency(s2, s3):
    S2.value = s2
    S3.value = s3
    time.sleep(0.1)

    start = time.time()
    for _ in range(10):
        OUT.wait_for_active()
        OUT.wait_for_inactive()
    duration = time.time() - start

    if duration == 0:
        return 0

    return 10 / duration  # Hz

try:
    while True:
        red = read_frequency(False, False)   # S2=0, S3=0
        green = read_frequency(True, True)   # S2=1, S3=1
        blue = read_frequency(False, True)   # S2=0, S3=1

        print(f"R: {red:.1f} Hz, G: {green:.1f} Hz, B: {blue:.1f} Hz")
        print("-------------")
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")
