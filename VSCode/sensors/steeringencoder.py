from gpiozero import RotaryEncoder
from signal import pause

# Adjust these based on your encoder + steering mechanism
STEPS_PER_FULL_LEFT = -50  # max step count when turning fully left
STEPS_PER_FULL_RIGHT = 50  # max step count when turning fully right
MAX_ANGLE = 30  # maximum steering angle in degrees (adjust to your car)

encoder = RotaryEncoder(a=5, b=6, max_steps=0)

def steps_to_angle(steps):
    # Clamp steps to the configured range
    steps = max(STEPS_PER_FULL_LEFT, min(STEPS_PER_FULL_RIGHT, steps))
    angle = (steps / STEPS_PER_FULL_RIGHT) * MAX_ANGLE
    return round(angle, 1)

def on_rotate():
    angle = steps_to_angle(encoder.steps)
    print(f"Steering angle: {angle}°")

encoder.when_rotated = on_rotate

print("Turn the steering (gently). Ctrl+C to stop.")
pause()
