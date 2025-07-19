import lgpio
import time
from gpiozero import DigitalOutputDevice


class myServo:
    def __init__(self, servo_pin, center_angle=90, max_deviation=30):
        self.chip = lgpio.gpiochip_open(0)
        self.servo_pin = servo_pin
        self.center = center_angle
        self.deviation = max_deviation
        self.pwm_freq = 50  # Hz
        lgpio.gpio_claim_output(self.chip, self.servo_pin)

    def angle_to_pulse(self, angle):
        # Clamp to 0–180, then convert to microseconds
        angle = max(0, min(180, angle))
        return int(500 + (angle / 180) * 2000)

    def set_servo_angle(self, relative_angle):
        # Clamp relative to center ± deviation
        absolute_angle = max(self.center - self.deviation,
                             min(self.center + self.deviation, self.center + relative_angle))
        pulse = self.angle_to_pulse(absolute_angle)
        lgpio.tx_pwm(self.chip, self.servo_pin, self.pwm_freq, pulse * 1e-6 * self.pwm_freq * 100)
        print(f"→ Angle: {absolute_angle}°, Pulse: {pulse}µs")

    def cleanup(self):
        lgpio.gpiochip_close(self.chip)

#servo = myServo(12, center_angle=75, max_deviation=30)

for _ in range(0): 
        
	for angle in [-30,-20,-10,0,10,20,30]:
                servo.set_servo_angle(angle)
                print(angle)
                time.sleep(1)

#servo.cleanup()
