from math import atan2, degrees, radians, cos, sin
from time import time, sleep
from ekf2class import EKFEstimator_NoEncoder
from CarController import CarController
from allEncodersClass import RobotEncoders
import matplotlib.pyplot as plt
import numpy as np

# Init
car = CarController(in1_pin=14, in2_pin=15, ena_pin=13, servo_pin=12)
encoders = RobotEncoders()
ekf = EKFEstimator_NoEncoder(wheelbase=13.0)

# Bezier setup: start (P0), end (P3), with heading theta3
P0 = np.array([0.0, 0.0])
P3 = np.array([120,0])
theta3 = radians(0)
P1 = P0 + 30 * np.array([1, 0])
P2 = P3 - 30 * np.array([cos(theta3), sin(theta3)])

def bezier(t):
    return (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3

def bezier_derivative(t):
    return 3 * (1 - t)**2 * (P1 - P0) + 6 * (1 - t) * t * (P2 - P1) + 3 * t**2 * (P3 - P2)

# Log and plot
positions = []
headings = []
timestamps = []
plt.ion()
fig, ax = plt.subplots()
ax.set_aspect("equal")

# Init pose
est = np.array([0.0, 0.0, 0.0])
positions.append((0.0, 0.0))
headings.append(0.0)
timestamps.append(0.0)

t_global_start = time()
speed_ratio = 0.8
t_bez = 0.0

try:
    while True:
        now = time()
        t_rel = now - t_global_start

        # Sensors
        v_l, v_r = encoders.get_linear_speeds()
        gyro_z = encoders.get_yaw_rate()

        v_cmd = 170 * (speed_ratio ** 2)
        est = ekf.update(
            local_pos=est,
            v_cmd=v_cmd,
            delta_cmd=radians(0),
            RRW=v_r,
            RLW=v_l,
            gyro_z_dps=gyro_z
        )

        x_cm = est[0]
        y_cm = -est[1]
        theta = -est[2]
        pos = np.array([x_cm, y_cm])

        positions.append((x_cm, y_cm))
        headings.append(theta)
        timestamps.append(t_rel)

        # Closest t on Bezier
        t_candidates = np.linspace(t_bez, min(t_bez + 0.1, 1.0), 10)
        distances = [np.linalg.norm(bezier(ti) - pos) for ti in t_candidates]
        t_bez = t_candidates[np.argmin(distances)]

        target = bezier(t_bez)
        tangent = bezier_derivative(t_bez)
        desired_angle = atan2(tangent[1], tangent[0])
        angle_error = atan2(sin(desired_angle - theta), cos(desired_angle - theta))

        to_goal = P3 - pos
        goal_facing = np.array([cos(theta3), sin(theta3)])
        projected = np.dot(to_goal, goal_facing)

        if projected < 0 or (np.linalg.norm(to_goal) < 3.0 and abs(angle_error) < radians(5)):
            car.brake(encoders)
            break

        # Stop if reached
        

        steer_deg = degrees(angle_error)
        steer_deg = max(-30, min(30, steer_deg+5))
        car.setAll("f", speed_ratio, steer_deg)

        # Plot
        ax.clear()
        bx, by = zip(*[bezier(ti) for ti in np.linspace(0, 1, 100)])
        ax.plot(bx, by, 'k--', label="Bezier")
        xs, ys = zip(*positions)
        ax.plot(xs, ys, 'b-', label="Robot")
        us = np.cos(headings)
        vs = np.sin(headings)
        ax.quiver(xs, ys, us, vs, scale=20, width=0.003, color='r')
        ax.legend()
        ax.set_title("Bezier Following")
        plt.pause(0.001)

        sleep(0.01)

    

except KeyboardInterrupt:
    car.stop()

plt.ioff()
plt.show()
