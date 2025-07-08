#parameters are 
# RRW linear speed from the encoder
#RLW linear speed from the encoder
#steering angle from the encoder
#linear and angular acceleration from the IMU
# I might use distance sensors and camera for recorrection

#the variables to estimate are[x, y, theta] 

import numpy as np
from filterpy.kalman import ExtendedKalmanFilter
import mpu6050  # MPU6050 driver: pip install mpu6050-raspberrypi
import time

L = 0.2  # wheelbase

# Init MPU6050
mpu = mpu6050.MPU6050(0x68)

# EKF setup
ekf = ExtendedKalmanFilter(dim_x=3, dim_z=3)
ekf.x = np.array([0., 0., 0.])
ekf.P *= 0.1
ekf.Q = np.eye(3) * 0.01
ekf.R = np.diag([0.05, 0.05, 0.02])  # Encoder + IMU fusion

#Predict the Car state based on the kinmetics modeling and command velocity and steering angle
def fx(x, dt, v, delta):
    x_, y_, theta = x
    dx = v * np.cos(theta) * dt
    dy = v * np.sin(theta) * dt
    dtheta = (v / L) * np.tan(delta) * dt
    return np.array([x_ + dx, y_ + dy, theta + dtheta])

#define the Jaicobian
def Fx_jacobian(x, dt, v, delta):
    _, _, theta = x
    return np.array([
        [1, 0, -v * np.sin(theta) * dt],
        [0, 1,  v * np.cos(theta) * dt],
        [0, 0, 1]
    ])

#Estimate the state based on the input data from the sensors
def hx(x):
    return x

# Loop
prev_time = time.time() #Save the current time for future calculations
theta_gyro = 0.0

while True:
    # --- Timing ---
    curr_time = time.time()
    dt = curr_time - prev_time
    prev_time = curr_time

    # --- Read inputs ---
    v_cmd = 1.0          # trajectory planner
    delta_cmd = 0.15     # trajectory planner
    RRW = 1.0            # measured
    RLW = 1.1
    delta_meas = 0.14
    v_meas = (RRW + RLW) / 2.0

    # --- Read gyro ---
    gyro_z = mpu.get_gyro_data()['z']  # degrees/sec
    gyro_z_rad = np.radians(gyro_z)
    theta_gyro += gyro_z_rad * dt

    # --- Predict using control command ---
    ekf.F = Fx_jacobian(ekf.x, dt, v_cmd, delta_cmd)
    ekf.predict(fx=fx, args=(dt, v_cmd, delta_cmd))

    # --- Correct using encoder + gyro drift heading ---
    x_enc = fx(ekf.x, dt, v_meas, delta_meas)
    x_enc[2] = theta_gyro  # overwrite with integrated IMU heading
    ekf.update(z=x_enc, HJacobian=None, Hx=hx)

    # --- Output ---
    print("Estimated Pose: x={:.2f}, y={:.2f}, θ={:.2f}".format(*ekf.x))
    time.sleep(0.05)
