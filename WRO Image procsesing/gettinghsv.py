import cv2
import numpy as np

def show_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv_frame = cv2.cvtColor(param, cv2.COLOR_BGR2HSV)
        h, s, v = hsv_frame[y, x]
        print(f"HSV at ({x}, {y}) -> H: {h}, S: {s}, V: {v}")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot open camera")
    exit()

cv2.namedWindow("HSV Inspector")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.setMouseCallback("HSV Inspector", show_hsv, frame)
    cv2.imshow("HSV Inspector", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
