from gpiozero import RotaryEncoder

class SteeringEncoder:
    def __init__(self, pin_a=5, pin_b=6, full_left=-50, full_right=50, max_angle=30):
        self.STEPS_PER_FULL_LEFT = full_left
        self.STEPS_PER_FULL_RIGHT = full_right
        self.MAX_ANGLE = max_angle

        self.encoder = RotaryEncoder(a=pin_a, b=pin_b, max_steps=0)

    def get_angle(self):
        steps = self.encoder.steps
        steps = max(self.STEPS_PER_FULL_LEFT, min(self.STEPS_PER_FULL_RIGHT, steps))
        angle = (steps / self.STEPS_PER_FULL_RIGHT) * self.MAX_ANGLE
        return round(angle, 1)

    def reset(self):
        self.encoder.steps = 0
