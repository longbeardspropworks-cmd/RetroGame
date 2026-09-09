import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from engine.tilemap import TileMap


def make_test_data():
    # 3x3 map: solid border, open center, one interior wall at (1, 0).
    ground = [[1, 1, 1] for _ in range(3)]
    collision = [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1],
    ]
    return {
        "tile_size": 16,
        "width": 3,
        "height": 3,
        "tileset": "unused",
        "layers": {"ground": ground, "collision": collision, "decoration": None, "foreground": None},
        "objects": [],
        "entities": [],
        "spawn_points": [{"name": "start", "x": 16, "y": 16}],
        "triggers": [{"name": "trigger", "x": 0, "y": 0, "width": 16, "height": 16}],
    }


class TileMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        # A single 16x16 tile is enough to slice for these tests.
        cls.tileset_surface = pygame.Surface((16, 16), pygame.SRCALPHA)

    def _make_tilemap(self):
        return TileMap(make_test_data(), self.tileset_surface)

    def test_solid_tiles_from_collision_layer(self):
        tilemap = self._make_tilemap()
        self.assertTrue(tilemap.is_solid(0, 0))
        self.assertFalse(tilemap.is_solid(1, 1))

    def test_out_of_bounds_counts_as_solid(self):
        tilemap = self._make_tilemap()
        self.assertTrue(tilemap.is_solid(-1, 0))
        self.assertTrue(tilemap.is_solid(3, 0))
        self.assertTrue(tilemap.is_solid(0, 3))

    def test_rect_collides_solid_detects_overlap(self):
        tilemap = self._make_tilemap()
        open_rect = pygame.Rect(20, 20, 4, 4)   # inside the open center tile
        wall_rect = pygame.Rect(0, 0, 4, 4)     # inside the border wall
        self.assertFalse(tilemap.rect_collides_solid(open_rect))
        self.assertTrue(tilemap.rect_collides_solid(wall_rect))

    def test_pixel_dimensions(self):
        tilemap = self._make_tilemap()
        self.assertEqual(tilemap.pixel_width, 48)
        self.assertEqual(tilemap.pixel_height, 48)

    def test_spawn_points_and_triggers_are_exposed(self):
        tilemap = self._make_tilemap()
        self.assertEqual(tilemap.spawn_points[0]["name"], "start")
        self.assertEqual(tilemap.triggers[0]["name"], "trigger")


if __name__ == "__main__":
    unittest.main()
