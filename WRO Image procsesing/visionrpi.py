from picamera2 import Picamera2
import cv2
from vision_system import Vision
import time

def take_action(obj):
    print(f"ACTION -> Reacting to {obj.color.upper()} | X={obj.x_cm:.1f} Y={obj.y_cm:.1f} Angle={obj.angle_horizontal:+.1f}°")

vs = Vision(debug=True)
picam2 = Picamera2()
picam2.preview_configuration.main.size = (3300, 2500)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(1)  # allow camera to warm up

print("Starting Lap 1, Side 1")
print("Press 'C' to simulate color sensor trigger")
print("Press 'Q' to quit\n")

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, 1)

    objects = vs.detect_obstacles(frame)

    if vs.lap_number == 1:
        for obj in objects:
            print(f"[LAP 1] {obj.color.upper()} | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")
        print(f"[LAP 1] SIGHT STATUS: {vs.sight}")

    elif vs.lap_number in [2, 3] and vs.side_number == 1:
        for obj in objects:
            if obj.color == "magenta":
                print(f"[LAP {vs.lap_number}] MAGENTA PARKING | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")

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

print("\nFinal Lap 1 Memory:")
for i, side in enumerate(vs.lap_memory):
    print(f"--- Side {i+1} ---")
    for obj in side:
        print(f"  {obj.color.upper()} | X: {obj.x_cm:.1f} | Y: {obj.y_cm:.1f} | Angle: {obj.angle_horizontal:+.1f}°")
        print(f"[LAP 1] {obj.color.upper()} | Initial X: {obj.initial_x_cm:.1f} cm | Initial Y: {obj.initial_y_cm:.1f} cm | "
              f"Current X: {obj.x_cm:.1f} cm | Current Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")



