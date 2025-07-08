from field_object import FieldObject

class ParkingLotMarker(FieldObject):  # or object if not subclassing
    def __init__(self, x_px, y_px, bbox, bbox_width_px, loop_count):
        super().__init__("magenta", x_px, y_px, bbox, bbox_width_px)
        self.marker_type = "parking"
        self.seen_at_loop = loop_count
        print(f"[DEBUG] Parking created at loop {loop_count}")

