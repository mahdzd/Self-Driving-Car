from gpiozero import RotaryEncoder
from signal import pause

# Adjust pins to match your wiring
encoder = RotaryEncoder(a=22, b=23, max_steps=0)

def turned_up():
    print("Clockwise")

def turned_down():
    print("Counterclockwise")

encoder.when_rotated_clockwise = turned_up
encoder.when_rotated_counter_clockwise = turned_down

print("Rotary encoder ready. Turn it slowly. Ctrl+C to stop.")
pause()
