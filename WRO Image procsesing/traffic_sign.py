from field_object import FieldObject

class TrafficSign(FieldObject):
    def __init__(self, color, x_px, y_px, bbox, bbox_width_px):
        super().__init__(color, x_px, y_px, bbox, bbox_width_px)

        # Define the direction based on color
        if color == "red":
            self.direction = "right"
        elif color == "green":
            self.direction = "left"
        else:
            self.direction = "unknown"
