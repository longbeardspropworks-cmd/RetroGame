import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from engine.tilemap import TileMap
from games.alphabet_excavation.excavator import Excavator, DIRT_TILE_ID, EXCAVATED_TILE_ID, DIG_DURATION


def make_tilemap():
    # 3x3, all dirt, nothing solid - enough to test digging in isolation.
    ground = [[DIRT_TILE_ID] * 3 for _ in range(3)]
    collision = [[0, 0, 0] for _ in range(3)]
    data = {
        "tile_size": 16,
        "width": 3,
        "height": 3,
        "tileset": "unused",
        "layers": {"ground": ground, "collision": collision, "decoration": None, "foreground": None},
        "objects": [],
        "entities": [],
        "spawn_points": [],
        "triggers": [],
    }
    tileset_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
    return TileMap(data, tileset_surface)


class FakeInput:
    """Minimal stand-in for InputManager: only the methods Excavator calls."""

    def __init__(self, pressed=None, just_pressed=None):
        self._pressed = pressed or set()
        self._just_pressed = just_pressed or set()

    def is_pressed(self, action):
        return action in self._pressed

    def is_just_pressed(self, action):
        return action in self._just_pressed


class ExcavatorDiggingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))  # needed for convert_alpha()

    def test_pressing_a_on_dirt_starts_digging(self):
        excavator = Excavator(16, 16)  # centered on tile (1, 1)
        tilemap = make_tilemap()
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)
        self.assertTrue(excavator.is_digging)

    def test_movement_is_ignored_while_digging(self):
        excavator = Excavator(16, 16)
        tilemap = make_tilemap()
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)
        excavator.handle_input(FakeInput(pressed={"RIGHT"}), tilemap)
        self.assertEqual(excavator.vx, 0.0)
        self.assertEqual(excavator.vy, 0.0)

    def test_tile_flips_to_excavated_after_dig_completes(self):
        excavator = Excavator(16, 16)
        tilemap = make_tilemap()
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)

        # Not yet finished partway through.
        excavator.update(DIG_DURATION / 2, tilemap)
        self.assertEqual(tilemap.get_ground_tile(1, 1), DIRT_TILE_ID)
        self.assertTrue(excavator.is_digging)

        # Finishes once the full duration has elapsed.
        excavator.update(DIG_DURATION / 2 + 0.01, tilemap)
        self.assertEqual(tilemap.get_ground_tile(1, 1), EXCAVATED_TILE_ID)
        self.assertFalse(excavator.is_digging)

    def test_pressing_a_on_already_excavated_tile_does_nothing(self):
        excavator = Excavator(16, 16)
        tilemap = make_tilemap()
        tilemap.set_ground_tile(1, 1, EXCAVATED_TILE_ID)
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)
        self.assertFalse(excavator.is_digging)

    def test_excavator_can_move_when_not_digging(self):
        excavator = Excavator(16, 16)
        tilemap = make_tilemap()
        excavator.handle_input(FakeInput(pressed={"RIGHT"}), tilemap)
        self.assertGreater(excavator.vx, 0)

    def test_pressing_a_again_mid_dig_does_not_restart_timer(self):
        excavator = Excavator(16, 16)
        tilemap = make_tilemap()
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)
        excavator.update(DIG_DURATION - 0.05, tilemap)
        excavator.handle_input(FakeInput(just_pressed={"A"}), tilemap)  # ignored: is_digging guard
        excavator.update(0.06, tilemap)
        self.assertFalse(excavator.is_digging)
        self.assertEqual(tilemap.get_ground_tile(1, 1), EXCAVATED_TILE_ID)


if __name__ == "__main__":
    unittest.main()
