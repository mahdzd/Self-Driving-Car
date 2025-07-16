class StopPID:
    def __init__(self, kp=1.2, ki=0.0, kd=0.2):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_sum = 0
        self.last_error = 0

    def reset(self):
        self.error_sum = 0
        self.last_error = 0

    def compute(self, v_l, v_r, dt):
        """
        Compute drive command to stop both wheels

        Args:
            v_l (float): left wheel speed (cm/s)
            v_r (float): right wheel speed (cm/s)
            dt (float): time step

        Returns:
            float: motor command (can be used symmetrically)
        """
        v_avg = 0.5 * (v_l + v_r)
        error = -v_avg  # target = 0
        self.error_sum += error * dt
        d_error = (error - self.last_error) / dt if dt > 0 else 0
        self.last_error = error

        return self.kp * error + self.ki * self.error_sum + self.kd * d_error
