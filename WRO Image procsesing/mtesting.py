import cv2
import numpy as np
from picamera2 import Picamera2

def show_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_frame = cv2.cvtColor(param, cv2.COLOR_BGR2HSV)
        h, s, v = hsv_frame[y, x]
        print(f"HSV at ({x}, {y}) -> H: {h}, S: {s}, V: {v}")

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

cv2.namedWindow("HSV Inspector")

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, 1)
    cv2.setMouseCallback("HSV Inspector", show_hsv, frame)
    cv2.imshow("HSV Inspector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
