from gpiozero import Button
from time import time, sleep
from threading import Thread

# === CONFIGURATION ===
PULSES_PER_REV = 20         # Adjust based on your encoder disk
WHEEL_CIRCUMFERENCE = 21.0  # cm (adjust based on your wheel)

# === GLOBALS ===
left_count = 0
right_count = 0
left_last_time = time()
right_last_time = time()
left_total_distance = 0.0
right_total_distance = 0.0

# === CALLBACKS ===
def left_pulse():
    global left_count, left_last_time, left_total_distance
    left_count += 1
    left_total_distance += WHEEL_CIRCUMFERENCE / PULSES_PER_REV
    left_last_time = time()

def right_pulse():
    global right_count, right_last_time, right_total_distance
    right_count += 1
    right_total_distance += WHEEL_CIRCUMFERENCE / PULSES_PER_REV
    right_last_time = time()

# === GPIO SETUP ===
left_sensor = Button(17, pull_up=True)
right_sensor = Button(27, pull_up=True)

left_sensor.when_pressed = left_pulse
right_sensor.when_pressed = right_pulse

# === SPEED MONITORING THREAD ===
def monitor_speed():
    global left_last_time, right_last_time
    while True:
        now = time()
        # Time since last pulse
        left_dt = now - left_last_time
        right_dt = now - right_last_time

        # Speed = Distance / Time per pulse
        left_speed = (WHEEL_CIRCUMFERENCE / PULSES_PER_REV) / left_dt if left_dt < 1 else 0
        right_speed = (WHEEL_CIRCUMFERENCE / PULSES_PER_REV) / right_dt if right_dt < 1 else 0

        print(f"[LEFT] Speed: {left_speed:.2f} cm/s | Distance: {left_total_distance:.2f} cm")
        print(f"[RIGHT] Speed: {right_speed:.2f} cm/s | Distance: {right_total_distance:.2f} cm")
        print("-" * 50)
        sleep(0.5)

# === START MONITOR THREAD ===
Thread(target=monitor_speed, daemon=True).start()

print("IR sensors tracking speed and distance. Rotate wheels. Ctrl+C to stop.")
try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    print("Stopped.")
