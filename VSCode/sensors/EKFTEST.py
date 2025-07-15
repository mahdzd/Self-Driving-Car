
from math import radians
from time import sleep
from EKFclass import EKFEstimator
from CarController import CarController
from allEncodersClass import RobotEncoders
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

positions = []


car = CarController(in1_pin=23, in2_pin=24, ena_pin=25, servo_pin=18)
ekf = EKFEstimator(wheelbase=0.2)
encoders = RobotEncoders()  # uses your combined class

try:
    car.setAll("f", 0.5, 25)  # Forward, 50% speed, turn right
    plt.ion()
    plt.figure()
    positions = []
    headings = []


    while True:
        # Read measurements
        v_l, v_r = encoders.get_linear_speeds()
        steer_deg = encoders.get_steering_angle()
        steer_rad = radians(steer_deg)

        # Simulated gyro value (replace with IMU reading if available)
        gyro_z = 45  # deg/sec

        # Update EKF
        est = ekf.update(
            local_pos=[0, 0, 0],
            v_cmd=0.5, delta_cmd=radians(25),
            RRW=v_r / 100, RLW=v_l / 100,
            delta_meas=steer_rad,
            gyro_z_dps=gyro_z
        )
       
        positions.append((est[0], est[1]))
        headings.append(est[2])  # theta

        # Extract data
        xs, ys = zip(*positions)
        us = [np.cos(t) * 0.1 for t in headings]  # arrow x-component
        vs = [np.sin(t) * 0.1 for t in headings]  # arrow y-component

        # Real-time plot
        plt.clf()
        plt.plot(xs, ys, 'b-', label="Trajectory")
        plt.quiver(xs, ys, us, vs, angles='xy', scale_units='xy', scale=1, color='r', width=0.004)
        plt.xlabel("x (m)")
        plt.ylabel("y (m)")
        plt.title("Real-Time EKF Position + Heading")
        plt.axis("equal")
        plt.legend()
        plt.pause(0.01)




        print(f"x={est[0]:.2f}, y={est[1]:.2f}, θ={np.degrees(est[2]):.1f}°")
        sleep(0.1)

except KeyboardInterrupt:
    car.stop()
    print("Stopped")
