class Barrier:
    def __init__(self, x_px, y_px, bbox_width_px, frame_width, distance_cm):
        self.color = "black"
        self.distance_cm = distance_cm
        self.x_px = x_px

        # Simple position classification based on x in frame
        if x_px < frame_width / 3:
            self.position = "left"
        elif x_px > 2 * frame_width / 3:
            self.position = "right"
        else:
            self.position = "front"

        self.bbox_width_px = bbox_width_px
