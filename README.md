# Retro Game Prototype

A lightweight retro 2D game engine/prototype targeting Raspberry Pi
3B/3B+, built with Python 3 and Pygame. See [CLAUDE.md](CLAUDE.md) for
the full project brief and architecture rules.

This is the **Initial Milestone**: a technical prototype only. There is
no character, story, or final art yet - just the engine scaffolding and
placeholder graphics/audio.

## Requirements

- Python 3.9+
- Pygame 2.5+

## Windows setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python tools/generate_assets.py
python main.py
```

`tools/generate_assets.py` writes the placeholder tileset, player
spritesheet, and sound/music files under `assets/`. Run it once after
installing dependencies (or any time you delete the `assets/` contents).

## Raspberry Pi 3B/3B+ setup

```bash
sudo apt update
sudo apt install python3 python3-pip python3-pygame
cd RetroGame
pip3 install -r requirements.txt   # only needed if python3-pygame is missing/outdated
python3 tools/generate_assets.py
python3 main.py
```

For a fullscreen kiosk-style launch on the Pi, set `"fullscreen": true`
in `data/settings.json`. If running without a desktop environment, you
may need to run under the console framebuffer (`SDL_VIDEODRIVER=kmsdrm`
or `SDL_VIDEODRIVER=fbcon`, depending on your OS image) - set this as an
environment variable before launching if the default SDL video driver
doesn't find a display.

## Controls

| Action | Keyboard          | Controller                  |
|--------|-------------------|------------------------------|
| Move   | Arrow keys / WASD | D-pad (digital, via axis 0/1)* |
| A      | Space / Z         | Button 1                    |
| B      | Left Shift / X    | Button 2                    |
| START  | Enter             | Button 9                    |
| SELECT | Tab               | Button 8                    |
| MENU   | Escape            | Button 9                    |

\* Verified against a generic USB "SNES-style" gamepad using
`tools/controller_diagnostic.py` - it reports its D-pad as two digital
axes (axis 0 = left/right, axis 1 = up/down), not a hat, and its face
buttons don't follow Xbox-style numbering. Button/axis numbers are not
standardized across controller models - if you use a different
controller and input doesn't respond correctly, run
`tools/controller_diagnostic.py` to read the real numbers for your
device and update `controls.controller` in `data/settings.json`
accordingly. The game is fully playable from the keyboard with no
controller connected.

Dev-only keys (not part of the logical input abstraction):
- **F1** - toggle the debug overlay
- **F11** - toggle fullscreen

## What's implemented (Initial Milestone)

1. 320x180 logical rendering, scaled to the window with integer
   nearest-neighbor scaling (crisp pixel art at any window size).
2. Resizable/fullscreen window (`F11` toggles at runtime).
3. Keyboard input via the `InputManager` abstraction.
4. USB controller input (buttons, D-pad hat) via the same abstraction;
   hotplug-aware.
5. A 30x20 tile test map (`data/maps/test_map.json`), larger than the
   320x180 screen, with ground/collision/decoration/foreground layers,
   a spawn point, and a trigger region.
6. A controllable placeholder test entity (`game/player.py`).
7. Solid tile collision with axis-separated sliding.
8. Camera following with configurable smoothing and map-bounds clamping.
9. Sprite-sheet animation (`engine/animation.py`), including deriving a
   "walk left" animation by flipping "walk right" frames.
10. Basic sound/music playback (`engine/audio.py`) that fails gracefully
    if the mixer or an asset is unavailable. Press **A** in-game to hear
    a sound effect; music loops automatically.
11. Pause state (press **START** or **Escape** during gameplay).
12. Debug overlay: FPS, current state, player world position, entity
    count, and a collision-box outline (toggle with **F1**).
13. Clean engine/game/data/assets project structure.
14. Windows setup instructions (above).
15. Raspberry Pi setup instructions (above).

## Known limitations / deferred work

- **Fonts**: text is drawn with Pygame's built-in system font as a
  placeholder. CLAUDE.md calls for an external bitmap/pixel font -
  swapping one in only requires changing `engine/ui.py`.
- **DIALOGUE / GAME_OVER states**: not yet implemented. The state
  machine (`engine/state.py`) supports adding them trivially when there
  is content that needs them.
- **Save system**: not part of this milestone; deferred until there is
  actual game progress worth persisting.
- **Camera dead zone**: camera currently re-centers continuously with
  smoothing; a configurable dead zone is a documented "eventually" in
  CLAUDE.md and hasn't been built yet.
- **High-speed tunneling**: tile collision resolves one tile of
  penetration per axis per frame, which is standard for this kind of
  game but could in theory be skipped over at very high speeds/low frame
  rates. Not a concern at the current movement speed.

## Tests

```bash
python -m unittest discover tests
```

Covers input mapping, collision resolution, camera math, tilemap
loading/collision, animation timing, and state machine transitions.
Visual/gameplay behavior (rendering, controller feel, audio) should be
verified by actually running the game.
