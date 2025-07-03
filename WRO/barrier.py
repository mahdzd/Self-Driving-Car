from field_object import FieldObject

class Barrier(FieldObject):
    def __init__(self, x_px, y_px, bbox, bbox_width_px):
        super().__init__("black", x_px, y_px, bbox, bbox_width_px)
        self.barrier_type = "wall"
