import cv2
import numpy as np
from picamera2 import Picamera2
import time

from traffic_sign import TrafficSign
from parking import ParkingLotMarker
from config import HSV_RANGES, REAL_WIDTH_CM, FOCAL_LENGTH_PX

object_registry = []

def match_or_create(color_label, cx, cy, bbox, bbox_width, frame_w, frame_h):
    threshold_px = 50
    for obj in object_registry:
        if obj.color == color_label and obj.alive:
            dist = np.linalg.norm([obj.x_px - cx, obj.y_px - cy])
            if dist < threshold_px:
                obj.update_position(cx, cy, bbox, bbox_width)
                obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[color_label], FOCAL_LENGTH_PX)
                return

    if color_label == "red":
        new_obj = TrafficSign(color_label, cx, cy, bbox, bbox_width)
    elif color_label == "red2":
        new_obj = TrafficSign("red", cx, cy, bbox, bbox_width)
    elif color_label == "green":
        new_obj = TrafficSign(color_label, cx, cy, bbox, bbox_width)
    elif color_label == "magenta":
        new_obj = ParkingLotMarker(cx, cy, bbox, bbox_width)
    else:
        return

    new_obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[new_obj.color], FOCAL_LENGTH_PX)
    object_registry.append(new_obj)

# === Setup Pi Camera ===
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1280, 720)}, raw={"size": picam2.sensor_resolution})
picam2.configure(config)
picam2.start()
time.sleep(1)

cv2.namedWindow("WRO Vision", cv2.WINDOW_NORMAL)
cv2.resizeWindow("WRO Vision", 1280, 720)

# === Main Loop ===
while True:
    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert to OpenCV format
    frame = cv2.flip(frame, 1)
    frame_h, frame_w = frame.shape[:2]

    for obj in object_registry:
        obj.alive = False

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    for color_label, (lower, upper) in HSV_RANGES.items():
        if color_label == "black":
            continue

        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) < 300:
                continue

            x, y, w, h = cv2.boundingRect(cnt)
            cx = x + w // 2
            cy = y + h // 2

            match_or_create(color_label, cx, cy, (x, y, w, h), w, frame_w, frame_h)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
            cv2.putText(frame, color_label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    for obj in object_registry:
        if not obj.alive:
            obj.mark_dead()

    for obj in object_registry:
        if obj.alive:
            label = (
                f"{obj.color} | X={obj.x_cm:.1f}cm Y={obj.y_cm:.1f}cm "
                f"D={obj.distance_cm:.1f}cm A={obj.angle_horizontal:.1f}°"
            )
            cv2.putText(frame, label,
                        (int(obj.x_px), int(obj.y_px) + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("WRO Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(object_registry)
cv2.destroyAllWindows()
