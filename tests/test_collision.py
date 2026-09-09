import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import collision


class FakeTileMap:
    """Minimal stand-in exposing only what collision.py needs, so these
    tests don't depend on loading a real tileset image from disk."""

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


class MoveWithTileCollisionTests(unittest.TestCase):
    def test_moves_freely_with_no_obstacles(self):
        tilemap = FakeTileMap(solid_cells=[])
        x, y = collision.move_with_tile_collision(10, 10, 8, 8, 5, 5, tilemap)
        self.assertEqual((x, y), (15, 15))

    def test_blocked_moving_right_snaps_to_wall(self):
        # Wall tile at column 2 (world x 32-47). Entity is 8px wide.
        tilemap = FakeTileMap(solid_cells=[(2, 0)])
        x, y = collision.move_with_tile_collision(20, 0, 8, 8, 20, 0, tilemap)
        self.assertEqual(x, 32 - 8)
        self.assertEqual(y, 0)

    def test_blocked_moving_left_snaps_to_wall(self):
        tilemap = FakeTileMap(solid_cells=[(1, 0)])
        x, y = collision.move_with_tile_collision(40, 0, 8, 8, -20, 0, tilemap)
        self.assertEqual(x, 32)  # right edge of tile column 1 (x=16..31) is 32
        self.assertEqual(y, 0)

    def test_sliding_along_wall_when_moving_diagonally(self):
        # Solid tile directly to the right; moving down should still work
        # even though moving right is blocked.
        tilemap = FakeTileMap(solid_cells=[(2, 0)])
        x, y = collision.move_with_tile_collision(20, 0, 8, 8, 20, 10, tilemap)
        self.assertEqual(x, 32 - 8)
        self.assertEqual(y, 10)

    def test_out_of_bounds_via_flag_is_not_checked_by_fake(self):
        # rects_overlap is a thin wrapper; just verify basic behavior.
        import pygame
        pygame.init()
        rect_a = collision.make_rect(0, 0, 10, 10)
        rect_b = collision.make_rect(5, 5, 10, 10)
        rect_c = collision.make_rect(100, 100, 10, 10)
        self.assertTrue(collision.rects_overlap(rect_a, rect_b))
        self.assertFalse(collision.rects_overlap(rect_a, rect_c))


if __name__ == "__main__":
    unittest.main()
