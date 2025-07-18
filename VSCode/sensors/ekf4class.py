import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import time

class EKFEstimator_SensorOnly:
    def __init__(self, wheelbase=0.13):
        self.wheelbase = wheelbase
        self.ekf = ExtendedKalmanFilter(dim_x=3, dim_z=3)  # [x, y, theta]

        self.ekf.x = np.array([0., 0., 0.])
        self.ekf.P *= 0.0
        self.ekf.Q = np.eye(3) * 0.01
        self.ekf.R = np.diag([0.01, 0.01, 0.002])

        self.prev_time = time.time()

    def _fx(self, x, dt, v, delta):
        x_, y_, theta = x
        dx = v * np.cos(theta) * dt
        dy = v * np.sin(theta) * dt
        dtheta = (v / self.wheelbase) * np.tan(delta) * dt
        return np.array([x_ + dx, y_ + dy, theta + dtheta])

    def _Fx_jacobian(self, x, dt, v, delta):
        _, _, theta = x
        return np.array([
            [1, 0, -v * np.sin(theta) * dt],
            [0, 1,  v * np.cos(theta) * dt],
            [0, 0, 1]
        ])

    def _hx(self, x):
        return x

    def update(self, v_l, v_r, delta_meas, imu_theta_rad):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time

        # Estimated forward velocity
        v = (v_l + v_r) / 2.0

        # Predict
        self.ekf.F = self._Fx_jacobian(self.ekf.x, dt, v, delta_meas)
        self.ekf.x = self._fx(self.ekf.x, dt, v, delta_meas)
        self.ekf.predict()

        # Update with sensor-based estimate
        x_meas = self.ekf.x.copy()
        x_meas[2] = imu_theta_rad  # replace yaw with IMU reading
        self.ekf.update(z=x_meas, HJacobian=lambda x: np.eye(3), Hx=self._hx)

        return self.ekf.x.copy()
