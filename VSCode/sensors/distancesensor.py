import RPi.GPIO as GPIO
import time

TRIG = 10  # GPIO 10
ECHO = 9   # GPIO 9

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def read_distance():
    # Ensure trigger is low
    GPIO.output(TRIG, False)
    time.sleep(0.05)

    # Send 10us pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo to go HIGH and record start time
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo to go LOW and record end time
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Pulse duration
    pulse_duration = pulse_end - pulse_start

    # Calculate distance (in cm)
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

try:
    while True:
        dist = read_distance()
        print(f"Distance: {dist} cm")
        time.sleep(0.2)

except KeyboardInterrupt:
    GPIO.cleanup()
