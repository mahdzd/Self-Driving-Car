import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import time

class EKFEstimator_NoEncoder:
    def __init__(self, wheelbase=14, axle_width=13 ):
        """
        wheelbase: distance between front and rear axle (in meters or cm)
        axle_width: distance between left and right rear wheels (for encoder-based yaw rate)
        """
        self.wheelbase = wheelbase
        self.axle_width = axle_width

        self.ekf = ExtendedKalmanFilter(dim_x=3, dim_z=3)
        self.ekf.x = np.array([0., 0., 0.])       # state: [x, y, theta]
        self.ekf.P *= 1                     # initial state uncertainty
        self.ekf.Q = np.eye(3) * 0.1             # process noise (model uncertainty)
        self.ekf.R = np.diag([0.082, 0.082, 0.082])       # measurement noise (sensor uncertainty)

        self.theta_gyro = 0.0                     # accumulated yaw from gyro
        self.theta_enc = 0.0                      # accumulated yaw from encoders
        self.prev_time = time.time()

    def _fx(self, x, dt, v, delta):
        """
        Motion model: predicts next state from current state, speed, and steering
        """
        x_, y_, theta = x
        dx = v * np.cos(theta) * dt
        dy = v * np.sin(theta) * dt
        dtheta = (v / self.wheelbase) * np.tan(delta) * dt
        return np.array([x_ + dx, y_ + dy, theta + dtheta])

    def _Fx_jacobian(self, x, dt, v, delta):
        """
        Jacobian of the motion model w.r.t state xs
        """
        _, _, theta = x
        return np.array([
            [1, 0, -v * np.sin(theta) * dt],
            [0, 1,  v * np.cos(theta) * dt],
            [0, 0, 1]
        ])

    def _hx(self, x):
        """
        Measurement function: direct observation of [x, y, theta]
        """
        return x

    def update(self, local_pos, v_cmd, delta_cmd, RRW, RLW, gyro_z_dps):
        """
        Run one EKF cycle
        Inputs:
            local_pos     : current estimate used as starting reference
            v_cmd         : commanded linear speed (used in model prediction)
            delta_cmd     : commanded steering angle (used in model prediction)
            RRW, RLW      : right and left rear wheel speeds (cm/s)
            gyro_z_dps    : yaw rate from IMU (deg/s)
        """
        # Compute dt
        curr_time = time.time()
        dt = curr_time - self.prev_time
        self.prev_time = curr_time

        # === Integrate yaw from gyro ===
        gyro_z_rad = np.radians(gyro_z_dps)
        self.theta_gyro += gyro_z_rad * dt

        # === Estimate yaw from encoder difference ===
        omega_enc = (RRW - RLW) / self.axle_width  # rad/s
        self.theta_enc += omega_enc * dt
        print(f"omega_enc = {(RRW - RLW):.2f} / {self.axle_width:.2f} = {omega_enc:.2f} rad/s")


        # === Prediction step ===
        self.ekf.F = self._Fx_jacobian(self.ekf.x, dt, v_cmd, delta_cmd)
        self.ekf.x = self._fx(self.ekf.x, dt, v_cmd, delta_cmd)
        self.ekf.predict()

        # === Estimate speed for measurement model ===
        v_meas = (RRW + RLW) / 2.0
        v_meas *= np.sign(v_cmd)

        # === Simulate motion from encoder-based speed ===
        x_enc = self._fx(self.ekf.x, dt, v_meas, delta_cmd)

        # === Blend yaw from gyro and encoder ===
        w_gyro = 0.6   # trust gyro more
        w_enc  = 0.4   # use encoder yaw to help
        theta_blend = w_gyro * self.theta_gyro + w_enc * self.theta_enc
        x_enc[2] = theta_blend  # overwrite theta in measurement

        # === Correction step ===
        self.ekf.update(z=x_enc, HJacobian=lambda x: np.eye(3), Hx=self._hx)

        return self.ekf.x.copy()
