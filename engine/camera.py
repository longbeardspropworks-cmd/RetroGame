"""Reusable camera: converts world coordinates into screen coordinates.

The camera never modifies world coordinates - it only tracks its own
top-left position in world space and offsets by that when asked to
convert. Follow behavior supports instant snapping or simple smoothing.
"""


class Camera:
    def __init__(self, viewport_width, viewport_height):
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.x = 0.0
        self.y = 0.0
        self.world_width = viewport_width
        self.world_height = viewport_height

    def set_world_bounds(self, world_width, world_height):
        self.world_width = world_width
        self.world_height = world_height

    def follow(self, target_x, target_y, smoothing=1.0):
        """Move toward centering the viewport on (target_x, target_y).

        smoothing=1.0 snaps instantly; smaller values ease toward the target.
        """
        desired_x = target_x - self.viewport_width / 2
        desired_y = target_y - self.viewport_height / 2
        self.x += (desired_x - self.x) * smoothing
        self.y += (desired_y - self.y) * smoothing
        self._clamp_to_bounds()

    def _clamp_to_bounds(self):
        max_x = max(0, self.world_width - self.viewport_width)
        max_y = max(0, self.world_height - self.viewport_height)
        self.x = min(max(self.x, 0), max_x)
        self.y = min(max(self.y, 0), max_y)

    def world_to_screen(self, world_x, world_y):
        return world_x - self.x, world_y - self.y
