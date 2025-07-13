import cv2
from vision_system import Vision

def take_action(obj):
    # Replace this with actual robot logic
    print(f"ACTION -> Reacting to {obj.color.upper()} | X={obj.x_cm:.1f} Y={obj.y_cm:.1f} Angle={obj.angle_horizontal:+.1f}°")
    # TODO : ACTION

vs = Vision(debug=True)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam")
    exit()

print("Starting Lap 1, Side 1")
print("Press 'C' to simulate color sensor trigger")
print("Press 'Q' to quit\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Vision only during lap 1
    objects = vs.detect_obstacles(frame)

    if vs.lap_number == 1:
        for obj in objects:
            print(f"[LAP 1] {obj.color.upper()} | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")
        print(f"[LAP 1] SIGHT STATUS: {vs.sight}")

    elif vs.lap_number in [2, 3] and vs.side_number == 1:
        for obj in objects:
            if obj.color == "magenta":
                print(f"[LAP {vs.lap_number}] MAGENTA PARKING | X: {obj.x_cm:.1f} cm | Y: {obj.y_cm:.1f} cm | Angle: {obj.angle_horizontal:+.1f}°")

    # Draw debug overlay
    cv2.imshow("Detection", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

    elif key == ord('c'):
        vs.next_side()

        # Perform memorized actions for Lap 2 and 3
        if vs.lap_number >= 2 and not vs.registry_done:
            print(f"\n🔁 Replaying Lap {vs.lap_number} - Side {vs.side_number}")
            if vs.side_number - 1 < len(vs.lap_memory):
                side_memory = vs.lap_memory[vs.side_number - 1]
                for obj in side_memory:
                    take_action(obj)

if cap.isOpened():
    cap.release()
cv2.destroyAllWindows()

# Summary of Lap 1 memory
print("\n Final Lap 1 Memory:")
for i, side in enumerate(vs.lap_memory):
    print(f"--- Side {i+1} ---")
    for obj in side:
        print(f"  {obj.color.upper()} | X: {obj.x_cm:.1f} | Y: {obj.y_cm:.1f} | Angle: {obj.angle_horizontal:+.1f}°")