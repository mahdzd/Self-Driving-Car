import cv2
import numpy as np
from traffic_sign import TrafficSign
from parking import ParkingLotMarker
from barrier import Barrier
from config import HSV_RANGES, REAL_WIDTH_CM, FOCAL_LENGTH_PX

class VisionSystem:
    def __init__(self):
        self.object_registry = []
        self.loop_count = 0
        self.corner_count = 0
        self.max_loops = 4
        self.parking_detected = False
        self.learned_trajectory = []
        self.cap = cv2.VideoCapture(0)

    def color_sensor_detects_line(self):
        return cv2.waitKey(1) & 0xFF == ord('c')

    def estimate_distance(self, real_width_cm, bbox_width_px, focal_length_px):
        if bbox_width_px == 0:
            return 0
        return (real_width_cm * focal_length_px) / bbox_width_px

    def execute_action(self, action):
        print(f"[ACTION] {action}")
        # TODO: Connect to motor control logic

    def match_or_create_barrier(self, cx, cy, bbox_width, frame_width, distance_cm):
        threshold_dist = 20
        position = None
        if cx < frame_width / 3:
            position = "left"
        elif cx > 2 * frame_width / 3:
            position = "right"
        else:
            position = "front"

        for obj in self.object_registry:
            if isinstance(obj, Barrier) and obj.position == position:
                if abs(obj.distance_cm - distance_cm) < threshold_dist:
                    obj.alive = True
                    obj.x_px = cx
                    obj.distance_cm = distance_cm
                    return

        new_barrier = Barrier(cx, cy, bbox_width, frame_width, distance_cm)
        self.object_registry.append(new_barrier)
        print(f"[NEW WALL] {position} @ {distance_cm:.1f}cm")

    def match_or_create(self, color_label, cx, cy, bbox, bbox_width, frame_w, frame_h):
        threshold_px = 50

        for obj in self.object_registry:
            if obj.color == color_label and obj.alive:
                dist = np.linalg.norm([obj.x_px - cx, obj.y_px - cy])
                if dist < threshold_px:
                    obj.update_position(cx, cy, bbox, bbox_width)
                    obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[color_label], FOCAL_LENGTH_PX)
                    return

        if color_label in {"red", "red2", "green"}:
            color = "red" if color_label == "red2" else color_label
            new_obj = TrafficSign(color, cx, cy, bbox, bbox_width)
            new_obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[color], FOCAL_LENGTH_PX)
            self.object_registry.append(new_obj)

        elif color_label == "magenta" and not self.parking_detected:
            new_obj = ParkingLotMarker(cx, cy, bbox, bbox_width, self.loop_count)
            new_obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM["magenta"], FOCAL_LENGTH_PX)
            self.parking_detected = True
            self.object_registry.append(new_obj)
            print(f"[INFO] Detected parking at loop {self.loop_count + 1}")

        elif color_label == "black":
            distance_cm = self.estimate_distance(REAL_WIDTH_CM["black"], bbox_width, FOCAL_LENGTH_PX)
            self.match_or_create_barrier(cx, cy, bbox_width, frame_w, distance_cm)

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        frame = cv2.flip(frame, 1)
        frame_h, frame_w = frame.shape[:2]

        if self.color_sensor_detects_line():
            self.corner_count += 1
            print(f"[DEBUG] Corner line detected. Total corners: {self.corner_count}")
            if self.corner_count % 4 == 0:
                self.loop_count += 1
                print(f"[INFO] Starting loop {self.loop_count + 1}")
                self.object_registry.clear()

        for obj in self.object_registry:
            obj.alive = False

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if self.loop_count == 0:
            for color_label, (lower, upper) in HSV_RANGES.items():
                if color_label not in {"red", "red2", "green", "magenta", "black"}:
                    continue
                if color_label == "magenta" and self.parking_detected:
                    continue

                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for cnt in contours:
                    x, y, w, h = cv2.boundingRect(cnt)
                    area = cv2.contourArea(cnt)
                    aspect_ratio = h / w if w != 0 else 0
                    if area < 400 or aspect_ratio < 1.2 or aspect_ratio > 3.5:
                        continue
                    cx = x + w // 2
                    cy = y + h // 2
                    self.match_or_create(color_label, cx, cy, (x, y, w, h), w, frame_w, frame_h)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    cv2.putText(frame, color_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            for obj in self.object_registry:
                if not obj.alive:
                    obj.mark_dead()

            alive_signs = [o for o in self.object_registry if isinstance(o, TrafficSign) and o.alive]
            if len(alive_signs) > 2:
                alive_signs.sort(key=lambda o: o.distance_cm)
                for sign in alive_signs[2:]:
                    sign.mark_dead()

            if len(alive_signs) == 2:
                sign_colors = [s.color for s in alive_signs]
                if "red" in sign_colors and "green" in sign_colors:
                    action = "drive_between"
                elif sign_colors.count("red") == 2:
                    action = "go_left"
                elif sign_colors.count("green") == 2:
                    action = "go_right"
                else:
                    action = "unknown"
                self.learned_trajectory.append({"signs": sign_colors, "action": action})
                print(f"[LEARNED] Lap {self.loop_count + 1}: {sign_colors} → {action}")
        else:
            if self.loop_count - 1 < len(self.learned_trajectory):
                action_to_repeat = self.learned_trajectory[self.loop_count - 1]["action"]
                self.execute_action(action_to_repeat)

        for obj in self.object_registry:
            if obj.alive:
                label = (
                    f"{obj.color} | X={obj.x_cm:.1f}cm Y={obj.y_cm:.1f}cm "
                    f"D={obj.distance_cm:.1f}cm A={obj.angle_horizontal:.1f}°"
                )
                cv2.putText(frame, label, (int(obj.x_px), int(obj.y_px) + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv2.putText(frame, f"Loop: {self.loop_count+1}/{self.max_loops} Corners: {self.corner_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

        cv2.imshow("WRO Vision", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            self.cap.release()
            cv2.destroyAllWindows()
            print("Final Learned Trajectory:", self.learned_trajectory)
            return False

        return True
