import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame
from engine.animation import load_spritesheet

# Reuses the real committed placeholder asset rather than a fixture -
# it's small, already part of the repo, and exercises the real file-load
# path (unlike a fake in-memory surface would).
PLAYER_SHEET_PATH = "assets/sprites/player.png"


class LoadSpritesheetCacheTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        pygame.display.set_mode((1, 1))  # needed for convert_alpha()

    def test_same_path_and_frame_size_returns_the_same_cached_object(self):
        first = load_spritesheet(PLAYER_SHEET_PATH, 16, 16)
        second = load_spritesheet(PLAYER_SHEET_PATH, 16, 16)
        self.assertIs(first, second)

    def test_different_frame_size_is_a_different_cache_entry(self):
        sheet_16 = load_spritesheet(PLAYER_SHEET_PATH, 16, 16)
        sheet_8 = load_spritesheet(PLAYER_SHEET_PATH, 8, 8)
        self.assertIsNot(sheet_16, sheet_8)
        self.assertEqual(sheet_8.frame_width, 8)


if __name__ == "__main__":
    unittest.main()
