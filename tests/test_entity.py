import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from engine.entity import Entity


class FakeTileMap:
    """Same minimal stand-in used in test_collision.py."""

    def __init__(self, solid_cells, tile_size=16):
        self.tile_size = tile_size
        self.solid_cells = set(solid_cells)

    def is_solid(self, tile_x, tile_y):
        return (tile_x, tile_y) in self.solid_cells

    def rect_collides_solid(self, rect):
        tile_size = self.tile_size
        min_tx = rect.left // tile_size
        max_tx = (rect.right - 1) // tile_size
        min_ty = rect.top // tile_size
        max_ty = (rect.bottom - 1) // tile_size
        for ty in range(min_ty, max_ty + 1):
            for tx in range(min_tx, max_tx + 1):
                if self.is_solid(tx, ty):
                    return True
        return False


class EntityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def test_collision_box_defaults_to_zero_size(self):
        entity = Entity(10, 20)
        rect = entity.get_collision_rect()
        self.assertEqual((rect.width, rect.height), (0, 0))

    def test_base_update_and_render_are_no_ops(self):
        entity = Entity(0, 0)
        entity.update(0.016)  # must not raise with no tilemap
        entity.update(0.016, tilemap=object())  # or with one
        entity.render(surface=None, camera=None)  # no animator set - must not raise

    def test_move_with_collision_moves_freely_with_no_obstacles(self):
        entity = Entity(10, 10, collision_width=8, collision_height=8)
        tilemap = FakeTileMap(solid_cells=[])
        entity.move_with_collision(5, 5, tilemap)
        self.assertEqual((entity.x, entity.y), (15, 15))

    def test_move_with_collision_is_blocked_by_a_solid_tile(self):
        entity = Entity(20, 0, collision_width=8, collision_height=8)
        tilemap = FakeTileMap(solid_cells=[(2, 0)])  # tile at world x 32-47
        entity.move_with_collision(20, 0, tilemap)
        self.assertEqual(entity.x, 32 - 8)

    def test_render_uses_animator_and_camera_when_present(self):
        class FakeAnimator:
            def current_surface(self):
                return "frame"

        class FakeCamera:
            def world_to_screen(self, x, y):
                return (x - 5, y - 5)

        class FakeSurface:
            def __init__(self):
                self.blits = []

            def blit(self, frame, pos):
                self.blits.append((frame, pos))

        entity = Entity(10, 10)
        entity.animator = FakeAnimator()
        surface = FakeSurface()
        entity.render(surface, FakeCamera())
        self.assertEqual(surface.blits, [("frame", (5, 5))])


if __name__ == "__main__":
    unittest.main()
