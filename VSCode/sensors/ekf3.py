from ekf2class import EKFEstimator_NoEncoder
from CarController import CarController
from allEncodersClass import RobotEncoders
import matplotlib.pyplot as plt
import numpy as np
from time import sleep, time
from math import radians

car = CarController(in1_pin=23, in2_pin=24, ena_pin=25, servo_pin=18)
ekf = EKFEstimator_NoEncoder(wheelbase=0.2)
encoders = RobotEncoders()

positions = []
headings = []

plt.ion()
plt.figure()

try:
    while True:
        v_l, v_r = encoders.get_linear_speeds()
        gyro_z = encoders.get_yaw_rate()

        est = ekf.update(
            local_pos=[0, 0, 0],
            v_cmd=(v_r + v_l) / 2 / 100,
            delta_cmd=radians(0),
            RRW=v_r / 100,
            RLW=v_l / 100,
            gyro_z_dps=gyro_z
        )

        positions.append((est[0], est[1]))
        headings.append(est[2])

        xs, ys = zip(*positions)
        us = [np.cos(t) * 0.1 for t in headings]
        vs = [np.sin(t) * 0.1 for t in headings]

        plt.clf()
        plt.plot(xs, ys, 'b-')
        plt.quiver(xs, ys, us, vs, angles='xy', scale_units='xy', scale=1, color='r', width=0.004)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("EKF Estimated Position (Free Movement)")
        plt.axis("equal")
        plt.pause(0.01)

        print(f"x={est[0]:.2f}, y={est[1]:.2f}, θ={np.degrees(est[2]):.1f}")
        sleep(0.1)

except KeyboardInterrupt:
    print("Stopped by user")

plt.ioff()
plt.show()
