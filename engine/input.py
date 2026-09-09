"""Input abstraction layer.

Game code must never reference raw pygame key codes or joystick button
indices directly - it asks the InputManager for the state of a logical
action (UP, DOWN, LEFT, RIGHT, A, B, START, SELECT, MENU) instead. This
keeps keyboard and controller mappings configurable from data and keeps
the game playable with either input source.
"""
import pygame

ACTIONS = ["UP", "DOWN", "LEFT", "RIGHT", "A", "B", "START", "SELECT", "MENU"]


class InputManager:
    def __init__(self, controls_config):
        self._keyboard_map = self._resolve_keyboard_map(controls_config.get("keyboard", {}))
        self._controller_map = controls_config.get("controller", {})
        self._joystick = self._open_first_joystick()

        self._current = {action: False for action in ACTIONS}
        self._previous = {action: False for action in ACTIONS}

    @staticmethod
    def _resolve_keyboard_map(raw_map):
        resolved = {}
        for action, key_names in raw_map.items():
            keys = []
            for name in key_names:
                key_code = getattr(pygame, name, None)
                if key_code is not None:
                    keys.append(key_code)
            resolved[action] = keys
        return resolved

    @staticmethod
    def _open_first_joystick():
        pygame.joystick.init()
        if pygame.joystick.get_count() > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return joystick
        return None

    def refresh_joystick(self):
        """Re-scan for a controller after a hotplug (connect/disconnect) event."""
        self._joystick = self._open_first_joystick()

    def has_controller(self):
        return self._joystick is not None

    def update(self):
        self._previous = dict(self._current)
        keys_pressed = pygame.key.get_pressed()
        for action in ACTIONS:
            pressed = any(keys_pressed[key_code] for key_code in self._keyboard_map.get(action, []))
            if not pressed and self._joystick is not None:
                pressed = self._is_controller_action_pressed(action)
            self._current[action] = pressed

    def _is_controller_action_pressed(self, action):
        for source in self._controller_map.get(action, []):
            kind = source.get("kind")
            if kind == "button":
                index = source["index"]
                if index < self._joystick.get_numbuttons() and self._joystick.get_button(index):
                    return True
            elif kind == "hat":
                hat_index = source.get("hat", 0)
                if hat_index >= self._joystick.get_numhats():
                    continue
                hat_x, hat_y = self._joystick.get_hat(hat_index)
                value = hat_x if source.get("axis") == "x" else hat_y
                if value == source.get("sign", 1):
                    return True
            elif kind == "axis":
                index = source["index"]
                if index < self._joystick.get_numaxes():
                    value = self._joystick.get_axis(index)
                    threshold = source.get("threshold", 0.5)
                    sign = source.get("sign", 1)
                    if value * sign > threshold:
                        return True
        return False

    def is_pressed(self, action):
        return self._current.get(action, False)

    def is_just_pressed(self, action):
        return self._current.get(action, False) and not self._previous.get(action, False)

    def is_just_released(self, action):
        return not self._current.get(action, False) and self._previous.get(action, False)
