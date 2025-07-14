
import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import time

class EKFEstimator:
    def __init__(self, wheelbase=0.2):
        # Vehicle physical parameter
        self.L = wheelbase

        # Init EKF
        self.ekf = ExtendedKalmanFilter(dim_x=3, dim_z=3)
        self.ekf.x = np.array([0., 0., 0.])   # Initial pose: x, y, theta
        self.ekf.P *= 0.1                    # Initial covariance
        self.ekf.Q = np.eye(3) * 0.01        # Process noise
        self.ekf.R = np.diag([0.05, 0.05, 0.02])  # Measurement noise

        # Internal state
        self.theta_gyro = 0.0
        self.prev_time = time.time()

    # Predict motion from commanded speed and steering angle
    def _fx(self, x, dt, v, delta):
        x_, y_, theta = x
        dx = v * np.cos(theta) * dt
        dy = v * np.sin(theta) * dt
        dtheta = (v / self.L) * np.tan(delta) * dt
        return np.array([x_ + dx, y_ + dy, theta + dtheta])

    # Jacobian of motion model
    def _Fx_jacobian(self, x, dt, v, delta):
        _, _, theta = x
        return np.array([
            [1, 0, -v * np.sin(theta) * dt],
            [0, 1,  v * np.cos(theta) * dt],
            [0, 0, 1]
        ])

    # Measurement function (identity)
    def _hx(self, x):
        return x

    # Call this to estimate position
    def update(self, local_pos, v_cmd, delta_cmd, RRW, RLW, delta_meas, gyro_z_dps):
        """
        local_pos: initial guess in local frame (x, y, theta)
        v_cmd: commanded speed (m/s)
        delta_cmd: commanded steering angle (rad)
        RRW/RLW: measured linear speeds of rear right/left wheels (m/s)
        delta_meas: measured steering angle from encoder (rad)
        gyro_z_dps: IMU angular velocity (deg/s) around Z
        """
        # Time delta
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time

        # Integrate IMU angular velocity
        gyro_z_rad = np.radians(gyro_z_dps)
        self.theta_gyro += gyro_z_rad * dt

        # Predict using commanded values
        self.ekf.F = self._Fx_jacobian(self.ekf.x, dt, v_cmd, delta_cmd)
        self.ekf.predict(fx=self._fx, args=(dt, v_cmd, delta_cmd))

        # Estimate true velocity
        v_meas = (RRW + RLW) / 2.0

        # Predict using encoder-measured motion
        x_enc = self._fx(self.ekf.x, dt, v_meas, delta_meas)
        x_enc[2] = self.theta_gyro  # Correct heading using IMU

        # Update EKF with sensor-based estimate
        self.ekf.update(z=x_enc, HJacobian=None, Hx=self._hx)

        return self.ekf.x.copy()  # Return estimated [x, y, theta]
