from picamera2 import Picamera2
import cv2
from vision_system import Vision
import time

# 🔁 GLOBAL VARIABLES
parking_exists = False
parking_location = [0, 0, 0]
pillars = []
lap_nb = 1
section_nb = 1

def take_action(obj):
    print(f"ACTION -> Reacting to {obj.color.upper()} | X={obj.x_cm:.1f} Y={obj.y_cm:.1f} Angle={obj.angle_horizontal:+.1f}°")

def run_vision_mission():
    global parking_exists, parking_location, pillars, lap_nb, section_nb

    vs = Vision(debug=True)
    picam2 = Picamera2()
    picam2.preview_configuration.main.size = (1000, 1000)
    picam2.preview_configuration.main.format = "RGB888"
    picam2.configure("preview")
    picam2.start()
    time.sleep(1)

    print("Starting Lap 1, Side 1")
    print("Press 'C' to simulate color sensor trigger")
    print("Press 'Q' to quit\n")

    while True:
        frame = picam2.capture_array()
        frame = cv2.flip(frame, 1)

        objects = vs.detect_obstacles(frame)

        # ✅ Update pillar data
        pillars = []
        for obj in objects:
            if obj.color in ["red", "green"]:
                pillars.append([obj.x_cm, obj.y_cm, obj.color, vs.side_number])

        # ✅ Update parking
        if vs.parking_marker and vs.side_number == 1 and vs.lap_number == 1:
            parking_exists = True
            parking_location = [vs.side_number, vs.parking_marker.x_cm, vs.parking_marker.y_cm]

        # ✅ Update lap and section
        lap_nb = vs.lap_number
        section_nb = vs.side_number

        # 🖨️ Debug info
        if vs.lap_number == 1:
            for obj in objects:
                print(f"[LAP 1] {obj.color.upper()} | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")
            print(f"[LAP 1] SIGHT STATUS: {vs.sight}")
        elif vs.lap_number in [2, 3] and vs.side_number == 1:
            for obj in objects:
                if obj.color == "magenta":
                    print(f"[LAP {vs.lap_number}] MAGENTA PARKING | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")

        # 🖼️ Show camera view
        cv2.imshow("Detection", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        elif key == ord('c'):
            vs.next_side()
            if vs.lap_number >= 2 and not vs.registry_done:
                print(f"\n🔁 Replaying Lap {vs.lap_number} - Side {vs.side_number}")
                if vs.side_number - 1 < len(vs.lap_memory):
                    side_memory = vs.lap_memory[vs.side_number - 1]
                    for obj in side_memory:
                        print(f"[LAP {vs.lap_number}] MEMORY {obj.color.upper()} | Updated X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")
                        take_action(obj)

    cv2.destroyAllWindows()
    picam2.stop()

    # 🖨️ Final memory log (still visible after 'q')
    print("\nFinal Lap 1 Memory:")
    for i, side in enumerate(vs.lap_memory):
        print(f"--- Side {i+1} ---")
        for obj in side:
            print(f"[LAP 1] {obj.color.upper()} | Initial X: {obj.initial_x_cm:.1f} | Initial Y: {obj.initial_y_cm:.1f} | "
                  f"Current X: {obj.x_cm:.1f} | Current Y: {obj.y_cm:.1f} | Angle: {obj.angle_horizontal:+.1f}°")

# ✅ Example usage
if __name__ == "__main__":
    run_vision_mission()

    # Now you can access the updated globals
    print("\n[UPDATED VALUES]")
    print("Parking Exists:", parking_exists)
    print("Parking Location:", parking_location)
    print("Pillars:", pillars)
    print("Lap:", lap_nb, "| Side:", section_nb)
