from gpiozero import DigitalOutputDevice, DigitalInputDevice
import time

# GPIO pin setup
S0 = DigitalOutputDevice(17)
S1 = DigitalOutputDevice(27)
S2 = DigitalOutputDevice(22)
S3 = DigitalOutputDevice(23)
OUT = DigitalInputDevice(24)

S0.on()   # 20% scaling
S1.off()

# Calibration values based on your data
FREQ_R = {'min': 4431, 'max': 30908}
FREQ_G = {'min': 1789, 'max': 30504}
FREQ_B = {'min': 2592, 'max': 22133}

# Map frequency to intensity (255 → high reflectivity)
def map_freq(f, fmin, fmax):
    f = min(max(f, fmin), fmax)
    return int((fmax - f) * 255 / (fmax - fmin))

# Read frequency
def read_frequency(s2_val, s3_val):
    S2.value = s2_val
    S3.value = s3_val
    time.sleep(0.1)
    start = time.time()
    for _ in range(10):
        OUT.wait_for_active()
        OUT.wait_for_inactive()
    return 10 / (time.time() - start)

# Get mapped intensity values
def get_rgb():
    rf = read_frequency(False, False)
    gf = read_frequency(True, True)
    bf = read_frequency(False, True)

    r = map_freq(rf, FREQ_R['min'], FREQ_R['max'])
    g = map_freq(gf, FREQ_G['min'], FREQ_G['max'])
    b = map_freq(bf, FREQ_B['min'], FREQ_B['max'])

    return r, g, b

# Classify color based on relative intensities
def classify_color(r, g, b):
    brightness = r + g + b

    if brightness < 100:
        return "black"
    elif brightness > 700:
        return "white"
    elif r > g and r > b:
        return "red"
    elif g > r and g > b:
        return "green"
    elif b > r and b > g:
        return "blue"
    else:
        return "unknown"

# Main loop
if __name__ == "__main__":
    try:
        while True:
            r, g, b = get_rgb()
            color = classify_color(r, g, b)
            print(f"R={r}, G={g}, B={b} → {color}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Stopped")
