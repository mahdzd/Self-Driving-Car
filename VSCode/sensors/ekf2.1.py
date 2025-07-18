from math import radians, cos, sin, degrees
from time import sleep, time
from ekf2class import EKFEstimator_NoEncoder
from CarController import CarController
from allEncodersClass import RobotEncoders
import matplotlib.pyplot as plt
import numpy as np

# Init
car = CarController(in1_pin=23, in2_pin=24, ena_pin=25, servo_pin=4)
encoders = RobotEncoders()
ekf = EKFEstimator_NoEncoder(wheelbase=13.0)
est = np.array([0.0, 0.0, 0.0])

positions = [(0.0, 0.0)]
headings = [0.0]
timestamps = [0.0]
t_global_start = time()

plt.ion()
fig, (ax_xy, ax_xt, ax_yt, ax_tt) = plt.subplots(4, 1, figsize=(6, 12))
fig.tight_layout(pad=3)

try:
    while True:
        try:
            cmd = input("Enter: speed steering duration (e.g. 0.5 -10 0.4) ? ")
            speed_ratio, steer_deg, move_time = map(float, cmd.strip().split())
        except:
            print("Invalid input. Try again.")
            continue
        car.setAll("b" if speed_ratio < 0 else "f", abs(speed_ratio), steer_deg)
        t0 = time()
        ekf.prev_time = time()  # Reset internal EKF timing

        while time() - t0 < move_time:
            now = time()
            t_rel = now - t_global_start

            v_l, v_r = encoders.get_linear_speeds()
            gyro_z = encoders.get_yaw_rate()

            v_cmd = 160 * (speed_ratio ** 2) * (-1 if speed_ratio < 0 else 1)

            est = ekf.update(
                local_pos=est,
                v_cmd=v_cmd,
                delta_cmd=radians(steer_deg),
                RRW=v_r,
                RLW=v_l,
                gyro_z_dps=gyro_z
            )

            x_cm, y_cm = est[0], -est[1]
            theta = -est[2]

            positions.append((x_cm, y_cm))
            headings.append(theta)
            timestamps.append(t_rel)

            xs, ys = zip(*positions)
            thetas_deg = [degrees(t) for t in headings]
            us = np.cos(headings)
            vs = np.sin(headings)

            # --- Plots ---
            ax_xy.clear()
            ax_xy.plot(xs, ys, 'b-')
            ax_xy.quiver(xs, ys, us, vs, scale=20, width=0.004, color='r')
            ax_xy.set_title("XY EKF Position")
            ax_xy.set_xlabel("x (cm)")
            ax_xy.set_ylabel("y (cm)")
            ax_xy.axis("equal")

            ax_xt.clear()
            ax_xt.plot(timestamps, xs, 'g-')
            ax_xt.set_title("x vs Time")
            ax_xt.set_xlabel("Time (s)")
            ax_xt.set_ylabel("x (cm)")

            ax_yt.clear()
            ax_yt.plot(timestamps, ys, 'm-')
            ax_yt.set_title("y vs Time")
            ax_yt.set_xlabel("Time (s)")
            ax_yt.set_ylabel("y (cm)")

            ax_tt.clear()
            ax_tt.plot(timestamps, thetas_deg, 'c-')
            ax_tt.set_title("? vs Time")
            ax_tt.set_xlabel("Time (s)")
            ax_tt.set_ylabel("? (deg)")

            plt.pause(0.001)
            print(f"x={x_cm:.1f} cm, y={y_cm:.1f} cm, ?={degrees(theta):.1f}")
            sleep(0.1)

        car.stop()

except KeyboardInterrupt:
    car.stop()
    print("Stopped")

plt.ioff()
plt.show()
