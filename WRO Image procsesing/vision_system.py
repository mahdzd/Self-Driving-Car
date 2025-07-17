import cv2
import numpy as np
from traffic_sign import TrafficSign
from parking import ParkingLotMarker
from config import HSV_RANGES, REAL_WIDTH_CM, FOCAL_LENGTH_PX

class Vision:
    def __init__(self, debug=False):
        self.debug = debug
        self.lap_number = 1
        self.side_number = 1
        self.max_laps = 3
        self.max_sides = 4
        self.lap_memory = []
        self.current_side_registry = []
        self.current_lap_registry = []
        self.registry_done = False
        self.freeze_processing = False
        self.side_initialized = False
        self.detection_frames = 0
        self.detection_frame_limit = 15
        self.sight = []
        self.parking_marker = None  # stores the single magenta marker from Lap 1   

    def reset_side_registry(self):
        self.current_side_registry = []
        self.side_initialized = False
        self.detection_frames = 0

    def detect_obstacles(self, frame):
        # Handle Lap 2/3 Side 1 for magenta parking
        allow_magenta_only = self.lap_number in [2, 3] and self.side_number == 1

        if  self.registry_done and not allow_magenta_only:
            if self.debug:
                status_text = f"Lap: {self.lap_number}/3 | Side: {self.side_number}/4 (Frozen)"
                cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            return []

        frame_h, frame_w = frame.shape[:2]
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        all_detections = []

        # Detect RED and GREEN signs
        for color in ["red", "red2", "green"]:
            lower, upper = HSV_RANGES[color]
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < 1000:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2
                label = "red" if "red" in color else "green"
                real_width = REAL_WIDTH_CM[label]
                distance_cm = (real_width * FOCAL_LENGTH_PX) / w

                all_detections.append({
                    "color": label,
                    "x_px": cx,
                    "y_px": cy,
                    "bbox": (x, y, w, h),
                    "bbox_width_px": w,
                    "distance_cm": distance_cm
                })

                if self.debug:
                    print(f"[DEBUG] Detected {label} at x={cx}, y={cy}, w={w}, distance={distance_cm:.1f}cm")

        # Step 1: Initial object registration (first N frames) 
        if not self.side_initialized and self.lap_number == 1:
            for det in all_detections:
                if len(self.current_side_registry) >= 2:
                    break

                matched = False
                for obj in self.current_side_registry:
                    dx = abs(det["x_px"] - obj.x_px)
                    dy = abs(det["y_px"] - obj.y_px)
                    if dx < 50 and dy < 50 and det["color"] == obj.color:
                        matched = True
                        break

                if not matched:
                    obj = TrafficSign(
                        color=det["color"],
                        x_px=det["x_px"],
                        y_px=det["y_px"],
                        bbox=det["bbox"],
                        bbox_width_px=det["bbox_width_px"]
                    )
                    obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[det["color"]], FOCAL_LENGTH_PX)
                    self.current_side_registry.append(obj)

            self.detection_frames += 1
            if self.detection_frames >= self.detection_frame_limit:
                self.side_initialized = True

        # Step 2: Update existing object geometry
        else:
            for obj in self.current_side_registry:
                obj.alive = False
                for det in all_detections:
                    dx = abs(det["x_px"] - obj.x_px)
                    dy = abs(det["y_px"] - obj.y_px)
                    if dx < 50 and dy < 50 and det["color"] == obj.color:
                        obj.update_position(det["x_px"], det["y_px"], det["bbox"], det["bbox_width_px"])
                        obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[det["color"]], FOCAL_LENGTH_PX)
                        obj.alive = True
                        break

        # DEBUG SIGHT PRINT
        if self.debug and self.lap_number == 1:
            self.sight = []
            for obj in self.current_side_registry:
                status = "ALIVE" if obj.alive else "DEAD"
                self.sight.append((obj.color, status))
            print(f"[DEBUG] SIGHT STATUS: {self.sight}")

        # OPTIONAL: Magenta Parking Detection (only Side 1 of each Lap)
        # if self.side_number == 1:
        #     lower, upper = HSV_RANGES["magenta"]
        #     mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
        #     kernel = np.ones((5, 5), np.uint8)
        #     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        #     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        #     contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #     for cnt in contours:
        #         area = cv2.contourArea(cnt)
        #         if area < 1000:
        #             continue
        #         x, y, w, h = cv2.boundingRect(cnt)
        #         cx, cy = x + w // 2, y + h // 2

        #         marker = ParkingLotMarker(cx, cy, (x, y, w, h), w, self.lap_number)
        #         marker.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM["magenta"], FOCAL_LENGTH_PX)

        #         if self.debug:
        #             cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
        #             label1 = f"MAGENTA {marker.distance_cm:.1f}cm"
        #             label2 = f"Angle: {marker.angle_horizontal:+.1f}"
        #             cv2.putText(frame, label1, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
        #             cv2.putText(frame, label2, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        #         # Only store magenta in Lap 1
        #         if self.side_number == 1:
        #             self.current_side_registry.append(marker)
        #         break  # Only one magenta detection

        # OPTIONAL: Magenta Parking Detection (only Side 1 of each Lap)
        if self.side_number == 1:
            lower, upper = HSV_RANGES["magenta"]
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area < 1000:
                    continue
                x, y, w, h = cv2.boundingRect(cnt)
                cx, cy = x + w // 2, y + h // 2

                if self.parking_marker is None and self.lap_number == 1:
                    # Store for first time
                    self.parking_marker = ParkingLotMarker(cx, cy, (x, y, w, h), w, self.lap_number)
                elif self.parking_marker:
                    # Update existing marker
                    self.parking_marker.update_position(cx, cy, (x, y, w, h), w)

                # Always update geometry
                if self.parking_marker:
                    self.parking_marker.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM["magenta"], FOCAL_LENGTH_PX)
                    
                    # Draw box in debug mode
                    if self.debug:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                        label1 = f"MAGENTA {self.parking_marker.distance_cm:.1f}cm"
                        label2 = f"Angle: {self.parking_marker.angle_horizontal:+.1f}"
                        cv2.putText(frame, label1, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                        cv2.putText(frame, label2, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

                break  # Only track one magenta per frame


        # UI Overlay
        if self.debug:
            for obj in self.current_side_registry:
                x, y, w, h = obj.bbox
                if obj.color == "red":
                    color_bgr = (0, 0, 255)
                elif obj.color == "green":
                    color_bgr = (0, 255, 0)
                elif obj.color == "magenta":
                    continue  # already drawn above
                else:
                    color_bgr = (255, 255, 255)

                cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
                label1 = f"{obj.color.upper()} {obj.distance_cm:.1f}cm"
                label2 = f"Angle: {obj.angle_horizontal:+.1f}"
                cv2.putText(frame, label1, (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)
                cv2.putText(frame, label2, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_bgr, 2)

            status_text = f"Lap: {self.lap_number}/3 | Side: {self.side_number}/4"
            cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # Update memory objects (Lap 2/3 sides)
        if self.lap_number >= 2 and self.side_number <= len(self.lap_memory):
            self.update_memory_objects(all_detections, frame_w, frame_h)

        return self.current_side_registry

    def update_memory_objects(self, new_detections, frame_w, frame_h):
        if self.lap_number < 2 or self.side_number > len(self.lap_memory):
            return

        memory_objects = self.lap_memory[self.side_number - 1]
        for obj in memory_objects:
            obj.alive = False  # Assume dead until matched

            for det in new_detections:
                if det["color"] != obj.color:
                    continue

                dx = abs(det["x_px"] - obj.x_px)
                dy = abs(det["y_px"] - obj.y_px)
                if dx < 50 and dy < 50:
                    obj.update_position(det["x_px"], det["y_px"], det["bbox"], det["bbox_width_px"])
                    obj.calculate_geometry(frame_w, frame_h, REAL_WIDTH_CM[det["color"]], FOCAL_LENGTH_PX)
                    obj.alive = True
                    break

    def next_side(self):
        if self.registry_done:
            return

        print(f"[INFO] Finished side {self.side_number} of lap {self.lap_number}")
        self.current_lap_registry.append(self.current_side_registry[:])
        self.side_number += 1
        self.reset_side_registry()

        if self.side_number > self.max_sides:
            print(f"[INFO] Completed lap {self.lap_number}")

            if self.lap_number == 1:
                self.lap_memory = self.current_lap_registry[:]
                self.freeze_processing = True

            self.lap_number += 1
            self.side_number = 1
            self.current_lap_registry = []

            if self.lap_number > self.max_laps:
                print("[INFO] All 3 laps completed. No more vision processing.")
                self.registry_done = True