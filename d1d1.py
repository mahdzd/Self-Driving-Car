from gpiozero import Button
from signal import pause

# Use GPIO17 and GPIO27 (you can change these)
left_sensor = Button(17, pull_up=True)
right_sensor = Button(27, pull_up=True)

left_count = 0
right_count = 0

def left_pulse():
    global left_count
    left_count += 1
    print(f"[LEFT] Pulse #{left_count}")

def right_pulse():
    global right_count
    right_count += 1
    print(f"[RIGHT] Pulse #{right_count}")

left_sensor.when_pressed = left_pulse
right_sensor.when_pressed = right_pulse

print("Both IR sensors active. Rotate wheels to test. Press Ctrl+C to stop.")
pause()  # Keep script running
