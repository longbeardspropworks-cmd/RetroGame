import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
from games.alphabet_excavation.states import Level1State
from games.alphabet_excavation.excavator import DIRT_TILE_ID, EXCAVATED_TILE_ID


class FakeRenderer:
    logical_width = 320
    logical_height = 180


class FakeGame:
    def __init__(self):
        self.renderer = FakeRenderer()
        self.debug = False


class Level1CompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))  # needed for convert_alpha() on load

    def _make_level(self):
        level = Level1State(FakeGame())
        level.enter()
        return level

    def test_not_complete_on_entry(self):
        level = self._make_level()
        self.assertFalse(level.is_complete)
        self.assertFalse(level._is_fully_excavated())

    def test_is_fully_excavated_once_no_dirt_remains(self):
        level = self._make_level()
        for row in level.tilemap.ground:
            for x in range(len(row)):
                if row[x] == DIRT_TILE_ID:
                    row[x] = EXCAVATED_TILE_ID
        self.assertTrue(level._is_fully_excavated())

    def test_update_flips_is_complete_once_fully_excavated(self):
        level = self._make_level()
        for row in level.tilemap.ground:
            for x in range(len(row)):
                if row[x] == DIRT_TILE_ID:
                    row[x] = EXCAVATED_TILE_ID
        level.update(1 / 60)
        self.assertTrue(level.is_complete)

    def test_partial_excavation_is_not_complete(self):
        level = self._make_level()
        # Dig exactly one dirt cell - the rest of the letter remains.
        for row in level.tilemap.ground:
            for x in range(len(row)):
                if row[x] == DIRT_TILE_ID:
                    row[x] = EXCAVATED_TILE_ID
                    level.update(1 / 60)
                    self.assertFalse(level.is_complete)
                    return
        self.fail("test map has no dirt tiles to dig")

    def test_render_does_not_crash_once_complete(self):
        level = self._make_level()
        level.is_complete = True
        surface = pygame.Surface((320, 180))
        level.render(surface)  # must not raise

    def test_debug_lines_report_completion_state(self):
        level = self._make_level()
        self.assertIn("COMPLETE: False", level.debug_lines())
        level.is_complete = True
        self.assertIn("COMPLETE: True", level.debug_lines())


if __name__ == "__main__":
    unittest.main()
