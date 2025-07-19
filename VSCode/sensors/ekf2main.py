from math import radians, cos, sin, degrees
from time import sleep, time
from ekf2class import EKFEstimator_NoEncoder
from CarController import CarController
from allEncodersClass import RobotEncoders
import matplotlib.pyplot as plt
import numpy as np
from gpiozero import DigitalOutputDevice

#servopin=DigitalOutputDevice(21)
#servopin.on()
# Init
car = CarController(in1_pin=14, in2_pin=15, ena_pin=13, servo_pin=12)
encoders = RobotEncoders()
ekf = EKFEstimator_NoEncoder(wheelbase=13.0)

commands = [(-0.7, 0)]

# Logs
positions = []
headings = []
timestamps = []

# Plot: 4 subplots
plt.ion()
fig, (ax_xy, ax_xt, ax_yt, ax_tt) = plt.subplots(4, 1, figsize=(6, 12))
fig.tight_layout(pad=3)

est = np.array([0.0, 0.0, 0.0])
positions = [(0.0, 0.0)]
headings = [0.0]
timestamps = [0.0]

t_global_start = time()

try:
    for speed_ratio, steer_deg in commands:
        car.setAll("b" if speed_ratio < 0 else "f", abs(speed_ratio), steer_deg)
        t0 = time()

        while time() - t0 < 1.5:
            now = time()
            t_rel = now - t_global_start

            v_l, v_r = encoders.get_linear_speeds()  # cm/s
            gyro_z = encoders.get_yaw_rate()         # deg/s

            v_cmd = 170 * (speed_ratio ** 2)
            if speed_ratio < 0:
                v_cmd *= -1

            est = ekf.update(
                local_pos=est,
                v_cmd=v_cmd,
                delta_cmd=radians(steer_deg),
                RRW=v_r,
                RLW=v_l,
                gyro_z_dps=gyro_z
            )
            

            # Invert Y and heading
            x_cm = est[0]
            y_cm = -est[1]               # invert value
            theta = -est[2]              # invert angle

            positions.append((x_cm, y_cm))
            headings.append(theta)
            timestamps.append(t_rel)

            xs, ys = zip(*positions)
            ts = timestamps
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
            ax_xt.plot(ts, xs, 'g-')
            ax_xt.set_title("x vs Time")
            ax_xt.set_xlabel("Time (s)")
            ax_xt.set_ylabel("x (cm)")

            ax_yt.clear()
            ax_yt.plot(ts, ys, 'm-')
            ax_yt.set_title("y vs Time (inverted)")
            ax_yt.set_xlabel("Time (s)")
            ax_yt.set_ylabel("y (cm)")

            ax_tt.clear()
            ax_tt.plot(ts, thetas_deg, 'c-')
            ax_tt.set_title("? vs Time (inverted)")
            ax_tt.set_xlabel("Time (s)")
            ax_tt.set_ylabel("? (deg)")

            plt.pause(0.001)
            print(f"x={x_cm:.1f} cm, y={y_cm:.1f} cm, ?={degrees(theta):.1f}")

            sleep(0.01)
        car.brake(encoders)

    
    #servopin.off()

except KeyboardInterrupt:
    car.stop()
    print("Stopped")

plt.ioff()
plt.show()
