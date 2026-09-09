import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame
from engine.input import InputManager, ACTIONS

CONTROLS_CONFIG = {
    "keyboard": {
        "UP": ["K_UP", "K_w"],
        "DOWN": ["K_DOWN", "K_s"],
        "LEFT": ["K_LEFT", "K_a"],
        "RIGHT": ["K_RIGHT", "K_d"],
        "A": ["K_SPACE"],
        "B": ["K_LSHIFT"],
        "START": ["K_RETURN"],
        "SELECT": ["K_TAB"],
        "MENU": ["K_ESCAPE"],
    },
    "controller": {},
}


class InputManagerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()

    def test_keyboard_map_resolves_key_names_to_pygame_codes(self):
        manager = InputManager(CONTROLS_CONFIG)
        self.assertIn(pygame.K_UP, manager._keyboard_map["UP"])
        self.assertIn(pygame.K_w, manager._keyboard_map["UP"])

    def test_unknown_key_name_is_skipped_not_crashed(self):
        config = {"keyboard": {"UP": ["K_UP", "NOT_A_REAL_KEY"]}, "controller": {}}
        manager = InputManager(config)
        self.assertEqual(manager._keyboard_map["UP"], [pygame.K_UP])

    def test_all_actions_default_to_not_pressed(self):
        manager = InputManager(CONTROLS_CONFIG)
        for action in ACTIONS:
            self.assertFalse(manager.is_pressed(action))

    def test_is_just_pressed_and_released_transitions(self):
        manager = InputManager(CONTROLS_CONFIG)
        # Simulate a press: previous=False, current=True.
        manager._previous["A"] = False
        manager._current["A"] = True
        self.assertTrue(manager.is_just_pressed("A"))
        self.assertFalse(manager.is_just_released("A"))

        # Simulate holding: previous=True, current=True.
        manager._previous["A"] = True
        self.assertFalse(manager.is_just_pressed("A"))

        # Simulate a release: previous=True, current=False.
        manager._current["A"] = False
        self.assertTrue(manager.is_just_released("A"))

    def test_update_does_not_crash_with_or_without_a_controller(self):
        # has_controller() legitimately depends on the machine running the
        # test (a real pad may or may not be plugged in) - what matters
        # here is that update() never raises either way.
        manager = InputManager(CONTROLS_CONFIG)
        manager.update()


if __name__ == "__main__":
    unittest.main()
