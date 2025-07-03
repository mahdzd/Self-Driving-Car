import uuid
import numpy as np

class FieldObject:
    # Static variables shared by all objects
    live_objects = 0
    all_objects = 0

    def __init__(self, color, x_px, y_px, bbox, bbox_width_px):
        self.id = uuid.uuid4()         # Unique identifier
        self.color = color             # Object color label
        self.x_px = x_px               # Object center X in pixels
        self.y_px = y_px               # Object center Y in pixels
        self.bbox = bbox               # (x, y, w, h)
        self.bbox_width_px = bbox_width_px  # Bounding box width (in pixels)
        self.alive = True              # Object is currently visible

        # Geometry-related attributes (will be calculated)
        self.x_cm = None               # Horizontal offset from center (cm)
        self.y_cm = None               # Forward distance from camera (cm)
        self.distance_cm = None       # Same as y_cm (optional alias)
        self.angle_horizontal = None  # Angle left/right (degrees)
        self.angle_vertical = None    # Angle up/down (degrees)

        # Increment shared counters
        FieldObject.live_objects += 1
        FieldObject.all_objects += 1

    def calculate_geometry(self, frame_width, frame_height, real_width_cm, focal_length_px):
        # Image center
        image_cx = frame_width // 2
        image_cy = frame_height // 2

        # Pixel offsets from center
        offset_x_px = self.x_px - image_cx
        offset_y_px = self.y_px - image_cy

        # Estimate forward distance (Y) using pinhole model
        self.distance_cm = (real_width_cm * focal_length_px) / self.bbox_width_px

        # Estimate real-world position relative to camera
        self.x_cm = (offset_x_px * self.distance_cm) / focal_length_px
        self.y_cm = self.distance_cm  # Same as distance forward

        # Estimate angles
        self.angle_horizontal = np.degrees(np.arctan2(self.x_cm, self.y_cm))
        self.angle_vertical = np.degrees(np.arctan2(offset_y_px, focal_length_px))

    def update_position(self, x_px, y_px, bbox, bbox_width_px):
        self.x_px = x_px
        self.y_px = y_px
        self.bbox = bbox
        self.bbox_width_px = bbox_width_px
        self.alive = True

    def mark_dead(self):
        if self.alive:
            self.alive = False
            FieldObject.live_objects -= 1
