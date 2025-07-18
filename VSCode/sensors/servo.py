from gpiozero import AngularServo
from time import sleep

# Connect signal pin to GPIO 12 (or another PWM-capable GPIO pin)
servo = AngularServo(13, min_angle=0, max_angle=180,
                     min_pulse_width=0.0005, max_pulse_width=0.0025)

# Allow servo to initialize
sleep(1)

# Set servo to a specific angle (e.g., 90 degrees)
servo.angle = 20
print("Servo moved to 90 degrees")

# Keep the program alive long enough to let servo move
sleep(2)

# Optional: stop the servo by removing the signal
servo.detach()  # Requires gpiozero >= 2.0
