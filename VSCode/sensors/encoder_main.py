from time import sleep
from allEncodersClass import RobotEncoders  # Replace with your file name if different

def main():
    encoders = RobotEncoders()

    print("📟 Live Speed & Yaw Monitor (Ctrl+C to stop)\n")

    try:
        while True:
            v_l, v_r = encoders.get_linear_speeds()
            omega_l, omega_r = encoders.get_angular_speeds()
            d_l, d_r = encoders.get_distances()
            yaw_rate = encoders.get_yaw_rate()

            print(f"🔁 Linear Speeds : Left = {v_l:.2f} cm/s | Right = {v_r:.2f} cm/s")
            print(f"🌀 Angular Speeds: Left = {omega_l:.2f} rad/s | Right = {omega_r:.2f} rad/s")
            print(f"📏 Distances     : Left = {d_l:.1f} cm | Right = {d_r:.1f} cm")
            print(f"🧭 Yaw Rate      : {yaw_rate:.2f} deg/s")
            print("-" * 60)

            sleep(0.2)

    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped.")

if __name__ == "__main__":
    main()
