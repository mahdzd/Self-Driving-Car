import RPi.GPIO as GPIO
import time

# Pin definitions
S0 = 21
S1 = 12
S2 = 14
S3 = 15
OUT = 4

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([S0, S1, S2, S3], GPIO.OUT)
GPIO.setup(OUT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Set frequency scaling to 20% (S0=1, S1=0)
GPIO.output(S0, GPIO.HIGH)
GPIO.output(S1, GPIO.LOW)

def read_frequency(color_label, s2_state, s3_state):
    GPIO.output(S2, s2_state)
    GPIO.output(S3, s3_state)
    time.sleep(0.1)  # allow sensor to settle

    start = time.time()
    pulses = 10
    for _ in range(pulses):
        GPIO.wait_for_edge(OUT, GPIO.FALLING)

    duration = time.time() - start
    frequency = pulses / duration
    print(f"{color_label}: {frequency:.2f} Hz")
    return frequency

try:
    while True:
        red = read_frequency("Red", GPIO.LOW, GPIO.LOW)
        green = read_frequency("Green", GPIO.HIGH, GPIO.HIGH)
        blue = read_frequency("Blue", GPIO.LOW, GPIO.HIGH)
        print("---")
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()