from field_object import FieldObject

class ParkingLotMarker(FieldObject):
    def __init__(self, x_px, y_px, bbox, bbox_width_px):
        super().__init__("magenta", x_px, y_px, bbox, bbox_width_px)
        self.marker_type = "parking"
