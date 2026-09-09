"""Centralized configuration loading.

All tunable values (display, controls, audio, debug) live in
data/settings.json instead of being scattered through the codebase.
Missing keys fall back to DEFAULT_SETTINGS so the game still runs with a
partial or missing settings file.
"""
import json
import os

DEFAULT_SETTINGS = {
    "display": {
        "logical_width": 320,
        "logical_height": 180,
        "window_width": 1280,
        "window_height": 720,
        "fullscreen": False,
        "window_title": "Game",
    },
    "fps": 60,
    "audio": {
        "master_volume": 1.0,
        "music_volume": 0.7,
        "sfx_volume": 0.8,
    },
    "debug": True,
    "controls": {
        "keyboard": {
            "UP": ["K_UP", "K_w"],
            "DOWN": ["K_DOWN", "K_s"],
            "LEFT": ["K_LEFT", "K_a"],
            "RIGHT": ["K_RIGHT", "K_d"],
            "A": ["K_SPACE", "K_z"],
            "B": ["K_LSHIFT", "K_x"],
            "START": ["K_RETURN"],
            "SELECT": ["K_TAB"],
            "MENU": ["K_ESCAPE"],
        },
        "controller": {
            "UP": [{"kind": "axis", "index": 1, "sign": -1}],
            "DOWN": [{"kind": "axis", "index": 1, "sign": 1}],
            "LEFT": [{"kind": "axis", "index": 0, "sign": -1}],
            "RIGHT": [{"kind": "axis", "index": 0, "sign": 1}],
            "A": [{"kind": "button", "index": 1}],
            "B": [{"kind": "button", "index": 2}],
            "START": [{"kind": "button", "index": 9}],
            "SELECT": [{"kind": "button", "index": 8}],
            "MENU": [{"kind": "button", "index": 9}],
        },
    },
}


def _merge_defaults(loaded, defaults):
    """Recursively fill in keys missing from `loaded` using `defaults`."""
    if not isinstance(loaded, dict):
        return defaults
    merged = dict(defaults)
    for key, value in loaded.items():
        if isinstance(value, dict) and isinstance(defaults.get(key), dict):
            merged[key] = _merge_defaults(value, defaults[key])
        else:
            merged[key] = value
    return merged


def load_settings(path="data/settings.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            loaded = json.load(f)
        return _merge_defaults(loaded, DEFAULT_SETTINGS)
    return json.loads(json.dumps(DEFAULT_SETTINGS))
