from time import sleep, time
import matplotlib.pyplot as plt
import numpy as np
from math import radians
from ekf4class import EKFEstimator_SensorOnly
from allEncodersClass import RobotEncoders

# EKF in centimeters
ekf = EKFEstimator_SensorOnly(wheelbase=13.0)
encoders = RobotEncoders()

positions = []
headings = []

plt.ion()
plt.figure()

try:
    while True:
        v_l, v_r = encoders.get_linear_speeds()  # must be in cm/s
        steering_deg = 0  # replace if available
        imu_theta_deg = 45  # simulate yaw

        est = ekf.update(
            v_l=v_l,
            v_r=v_r,
            delta_meas=radians(steering_deg),
            imu_theta_rad=radians(imu_theta_deg)
        )

        positions.append((est[0], est[1]))
        headings.append(est[2])

        xs, ys = zip(*positions)
        us = [np.cos(t) for t in headings]
        vs = [np.sin(t) for t in headings]

        plt.clf()
        plt.plot(xs, ys, 'b-')
        plt.quiver(xs, ys, us, vs, angles='xy', scale=10, color='r', width=0.004)
        plt.xlabel("x (cm)")
        plt.ylabel("y (cm)")
        plt.title("EKF Position Estimate (Sensor Only)")
        plt.axis("equal")
        plt.pause(0.01)

        print(f"x={est[0]:.1f} cm, y={est[1]:.1f} cm, θ={np.degrees(est[2]):.1f}°")
        sleep(0.1)

except KeyboardInterrupt:
    print("Stopped")

plt.ioff()
plt.show()
