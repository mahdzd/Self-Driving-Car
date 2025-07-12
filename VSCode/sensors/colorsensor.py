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

def detect_main_color():
    # === Step 1: Read color frequencies ===
    red_freq = read_frequency(False, False)
    green_freq = read_frequency(True, True)
    blue_freq = read_frequency(False, True)

    # === Step 2: Convert frequency to intensity ===
    # Assumes lower frequency means stronger reflected light
    red = 1000 / red_freq if red_freq else 0
    green = 1000 / green_freq if green_freq else 0
    blue = 1000 / blue_freq if blue_freq else 0

    rgb = [red, green, blue]

    # === Step 3: WRO Color Reference RGB Values ===
    def color_distance(c1, c2):
        return sum((a - b) ** 2 for a, b in zip(c1, c2))

    color_refs = {
        "orange": [255, 102, 0],
        "blue": [0, 51, 153],
        "grey": [179, 179, 179],
        "yellow": [255, 255, 0],
        "white": [255, 255, 255],
    }

    best_match = min(color_refs.items(), key=lambda item: color_distance(rgb, item[1]))
    return best_match[0]  # returns color name