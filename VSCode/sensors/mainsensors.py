from sensors import Sensors
import time

def main():
    sensors = Sensors()

    if not sensors.ready:
        print("[ERROR] Some sensors failed to initialize.")
        print(f"Distance Ready: {sensors.ready_distance}")
        print(f"Color Ready: {sensors.ready_color}")
        print(f"IMU Ready: {sensors.ready_imu}")
        return

    print("[INFO] All selected sensors initialized successfully.\n")

    try:
        while True:
            # Distance readings from 4 VL53L0X sensors
            distances = sensors.read_distances()
            print(f"[DISTANCES] {distances}")

            # Color detection
            color = sensors.read_color()
            print(f"[COLOR] {color}")

            # IMU readings
            imu_data = sensors.read_imu()
            if imu_data:
                accel, gyro = imu_data
                print(f"[IMU - Accel] {accel}")
                print(f"[IMU - Gyro] {gyro}")
            else:
                print("[IMU] Failed to read")

            print("-" * 50)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[INFO] Sensor test stopped by user.")

if __name__ == "__main__":
    main()
