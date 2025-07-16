from gpiozero import RotaryEncoder
from time import sleep

steering_encoder = RotaryEncoder(a=5, b=6, max_steps=20)

try:
    while True:
        print(f"Steps: {steering_encoder.steps}")
        sleep(0.1)
except KeyboardInterrupt:
    print("Stopped")

