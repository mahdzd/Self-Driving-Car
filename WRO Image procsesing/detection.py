import cv2
import numpy as np

# === Parameters ===
FOCAL_LENGTH_PX = 700  # Calibrate for your camera
REAL_WIDTH_CM = {
    "Red": 5.0,
    "Green": 5.0,
    "Magenta": 5.0
}
CAMERA_FOV_X = 60  # degrees
CAMERA_FOV_Y = 45  # degrees

# === Color settings ===
COLOR_SETTINGS = {
    "Red1": {
        "lower": [0, 150, 100], "upper": [10, 255, 255],
        "bgr": (0, 0, 255), "thresh": 1500, "label": "Red"
    },
    "Red2": {
        "lower": [170, 150, 100], "upper": [180, 255, 255],
        "bgr": (0, 0, 255), "thresh": 1500, "label": "Red"
    },
    "Green": {
        "lower": [35, 100, 100], "upper": [85, 255, 255],
        "bgr": (0, 255, 0), "thresh": 500, "label": "Green"
    },
    "Magenta": {
        "lower": [125, 50, 50], "upper": [165, 255, 255],
        "bgr": (255, 0, 255), "thresh": 300, "label": "Magenta"
    }
}

# === Detection Function ===
def detect_object(frame, hsv, color_name, settings, center_x, center_y, frame_w, frame_h):
    lower = np.array(settings["lower"])
    upper = np.array(settings["upper"])
    mask = cv2.inRange(hsv, lower, upper)

    # Clean up
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < settings["thresh"]:
            continue

        # Bounding box
        x, y, w, h = cv2.boundingRect(cnt)
        cx, cy = x + w // 2, y + h // 2

        # Distance (Y)
        real_width = REAL_WIDTH_CM[settings["label"]]
        distance_cm = (real_width * FOCAL_LENGTH_PX) / w

        # X coordinate in cm
        x_offset_px = cx - center_x
        x_cm = (x_offset_px * distance_cm) / FOCAL_LENGTH_PX

        # Angles
        angle_x = (x_offset_px / frame_w) * CAMERA_FOV_X
        y_offset_px = cy - center_y
        angle_y = -(y_offset_px / frame_h) * CAMERA_FOV_Y  # Negative because image Y increases downward

        # Draw box and crosshair
        cv2.rectangle(frame, (x, y), (x + w, y + h), settings["bgr"], 2)
        info_text = f"{settings['label']}: X={x_cm:.1f}cm Y={distance_cm:.1f}cm"
        angle_text = f"Angle: {angle_x:+.1f}°, {angle_y:+.1f}°"
        cv2.putText(frame, info_text, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, settings["bgr"], 2)
        cv2.putText(frame, angle_text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, settings["bgr"], 2)

        # Print info
        print(f"{settings['label']} -> X: {x_cm:.1f} cm, Y: {distance_cm:.1f} cm, "
              f"AngleX: {angle_x:+.1f}°, AngleY: {angle_y:+.1f}°")

        break  # One object per color

# === Main Loop ===
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame_h, frame_w = frame.shape[:2]
    center_x, center_y = frame_w // 2, frame_h // 2

    # Blur + HSV
    blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Crosshairs
    cv2.line(frame, (center_x, 0), (center_x, frame_h), (255, 0, 0), 2)
    cv2.line(frame, (0, center_y), (frame_w, center_y), (255, 0, 0), 2)

    # Run detection for each color
    for name, settings in COLOR_SETTINGS.items():
        detect_object(frame, hsv, name, settings, center_x, center_y, frame_w, frame_h)

    cv2.imshow("Full Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
