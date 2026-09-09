import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.camera import Camera


class CameraTests(unittest.TestCase):
    def test_world_to_screen_offsets_by_camera_position(self):
        camera = Camera(320, 180)
        camera.x = 50
        camera.y = 20
        self.assertEqual(camera.world_to_screen(100, 100), (50, 80))

    def test_follow_snaps_instantly_with_smoothing_one(self):
        camera = Camera(320, 180)
        camera.set_world_bounds(2000, 2000)
        camera.follow(1000, 1000, smoothing=1.0)
        self.assertEqual(camera.x, 1000 - 160)
        self.assertEqual(camera.y, 1000 - 90)

    def test_follow_clamps_to_map_bounds(self):
        camera = Camera(320, 180)
        camera.set_world_bounds(400, 300)
        # Target near the top-left corner: camera should clamp to (0, 0),
        # not go negative.
        camera.follow(10, 10, smoothing=1.0)
        self.assertEqual(camera.x, 0)
        self.assertEqual(camera.y, 0)

        # Target near the bottom-right corner: camera should clamp so the
        # viewport never shows past the map edge.
        camera.follow(390, 290, smoothing=1.0)
        self.assertEqual(camera.x, 400 - 320)
        self.assertEqual(camera.y, 300 - 180)

    def test_follow_clamps_when_map_smaller_than_viewport(self):
        camera = Camera(320, 180)
        camera.set_world_bounds(100, 100)
        camera.follow(50, 50, smoothing=1.0)
        self.assertEqual(camera.x, 0)
        self.assertEqual(camera.y, 0)

    def test_world_coordinates_are_never_mutated(self):
        camera = Camera(320, 180)
        camera.set_world_bounds(2000, 2000)
        target = (500, 500)
        camera.follow(*target, smoothing=1.0)
        self.assertEqual(target, (500, 500))


if __name__ == "__main__":
    unittest.main()
