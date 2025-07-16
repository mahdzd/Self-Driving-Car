from gpiozero import Button, RotaryEncoder
from time import time

class RobotEncoders:
    def __init__(self,
                 wheel_left_pin=17, wheel_right_pin=27,
                 pulses_per_rev=20, wheel_circ_cm=21.0,
                 steer_a=5, steer_b=6,
                 full_left=-50, full_right=50, max_angle=30):
        
        # Wheel encoder config
        self.PULSES_PER_REV = pulses_per_rev
        self.WHEEL_CIRC = wheel_circ_cm

        self.left_count = 0
        self.right_count = 0
        self.left_last_time = time()
        self.right_last_time = time()
        self.left_total_distance = 0.0
        self.right_total_distance = 0.0

        # Setup GPIO buttons for wheel encoders
        self.left_sensor = Button(wheel_left_pin, pull_up=True)
        self.right_sensor = Button(wheel_right_pin, pull_up=True)
        self.left_sensor.when_pressed = self._left_pulse
        self.right_sensor.when_pressed = self._right_pulse

        # Steering encoder config
        self.STEPS_FULL_LEFT = full_left
        self.STEPS_FULL_RIGHT = full_right
        self.MAX_STEER_ANGLE = max_angle
        self.steering_encoder = RotaryEncoder(a=steer_a, b=steer_b, max_steps=0)

    # --- Wheel Callbacks ---
    def _left_pulse(self):
        self.left_count += 1
        self.left_total_distance += self.WHEEL_CIRC / self.PULSES_PER_REV
        self.left_last_time = time()

    def _right_pulse(self):
        self.right_count += 1
        self.right_total_distance += self.WHEEL_CIRC / self.PULSES_PER_REV
        self.right_last_time = time()

    # --- Wheel Methods ---
    def get_linear_speeds(self):
        now = time()
        dt_l = now - self.left_last_time
        dt_r = now - self.right_last_time

        v_l = (self.WHEEL_CIRC / self.PULSES_PER_REV) / dt_l if dt_l < 1 else 0
        v_r = (self.WHEEL_CIRC / self.PULSES_PER_REV) / dt_r if dt_r < 1 else 0
        return v_l, v_r  # cm/s

    def get_angular_speeds(self):
        now = time()
        dt_l = now - self.left_last_time
        dt_r = now - self.right_last_time

        rev_l = 1 / self.PULSES_PER_REV / dt_l if dt_l < 1 else 0
        rev_r = 1 / self.PULSES_PER_REV / dt_r if dt_r < 1 else 0

        omega_l = 2 * 3.1416 * rev_l  # rad/s
        omega_r = 2 * 3.1416 * rev_r
        return omega_l, omega_r

    def get_distances(self):
        return self.left_total_distance, self.right_total_distance  # cm

    def reset_wheels(self):
        self.left_count = 0
        self.right_count = 0
        self.left_total_distance = 0
        self.right_total_distance = 0
        self.left_last_time = time()
        self.right_last_time = time()

    # --- Steering Methods ---
    def get_steering_angle(self):
        steps = self.steering_encoder.steps
        steps = max(self.STEPS_FULL_LEFT, min(self.STEPS_FULL_RIGHT, steps))
        angle = (steps / self.STEPS_FULL_RIGHT) * self.MAX_STEER_ANGLE
        return round(angle, 1)  # degrees

    def reset_steering(self):
        self.steering_encoder.steps = 0

    # --- All Reset ---
    def reset_all(self):
        self.reset_wheels()
        self.reset_steering()
    
    def get_motion_state(self):
        """
        Returns:
            dict: {
                'steering_angle': float (degrees),
                'left_speed': float (cm/s),
                'right_speed': float (cm/s)
            }
        """
        v_l, v_r = self.get_linear_speeds()
        angle = self.get_steering_angle()
        return {
            "steering_angle": angle,
            "left_speed": v_l,
            "right_speed": v_r
        }
