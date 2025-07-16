import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import time

class EKFEstimator_NoEncoder:
    def __init__(self, wheelbase=0.2):
        self.wheelbase = wheelbase
        self.ekf = ExtendedKalmanFilter(dim_x=3, dim_z=3)

        self.ekf.x = np.array([0., 0., 0.])       # [x, y, theta]
        self.ekf.P *= 0.1                         # initial uncertainty
        self.ekf.Q = np.eye(3) * 0.01             # process noise
        self.ekf.R = np.diag([0.05, 0.05, 0.02])  # measurement noise

        self.theta_gyro = 0.0
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

    def update(self, local_pos, v_cmd, delta_cmd, RRW, RLW, gyro_z_dps):
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time

        # Integrate yaw from gyro
        gyro_z_rad = np.radians(gyro_z_dps)
        self.theta_gyro += gyro_z_rad * dt

        # Prediction step
        self.ekf.F = self._Fx_jacobian(self.ekf.x, dt, v_cmd, delta_cmd)
        self.ekf.x = self._fx(self.ekf.x, dt, v_cmd, delta_cmd)
        self.ekf.predict()

        # Measurement from encoders + gyro
        v_meas = (RRW + RLW) / 2.0
        x_enc = self._fx(self.ekf.x, dt, v_meas, delta_cmd)
        x_enc[2] = self.theta_gyro  # replace heading with gyro yaw

        # Correction step
        self.ekf.update(z=x_enc, HJacobian=lambda x: np.eye(3), Hx=self._hx)


        return self.ekf.x.copy()
