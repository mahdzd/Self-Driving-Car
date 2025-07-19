import matplotlib.pyplot as plt
from time import time, sleep
from allEncodersClass import RobotEncoders
from CarController import CarController

car = CarController(in1_pin=14, in2_pin=15, ena_pin=13, servo_pin=12)
encoders = RobotEncoders()

times = []
v_left_list = []
v_right_list = []

def log_fn(t, v_l, v_r):
    times.append(t - start)
    v_left_list.append(v_l)
    v_right_list.append(v_r)

car.setAll("f", 1, -3)
start = time()
while time() - start < 2:
    t = time() - start
    v_l, v_r = encoders.get_linear_speeds()
    times.append(t)
    v_left_list.append(v_l)
    v_right_list.append(v_r)
    sleep(0.05)

car.brake(encoders, log_fn=log_fn)

plt.plot(times, v_left_list, label='Left Wheel')
plt.plot(times, v_right_list, label='Right Wheel')
plt.axvline(x=2.5, color='gray', linestyle='--', label='Brake Start')
plt.xlabel("Time (s)")
plt.ylabel("Velocity (cm/s)")
plt.legend()
plt.title("Wheel Velocities Before and During Brake")
plt.grid()
plt.show()
