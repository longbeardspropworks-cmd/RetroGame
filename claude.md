# Retro 2D Game — Claude Code Project Instructions

## Project Goal

Build a lightweight retro 2D game for Raspberry Pi 3B/3B+ using Python 3 and
Pygame.

Development happens primarily on Windows. The same source code must run on
Windows and Raspberry Pi Linux.

The project should favor:
- Simple, readable Python
- Fast iteration
- Data-driven game content
- Minimal dependencies
- Easy modification by an AI coding agent
- Reliable performance on Raspberry Pi 3B/3B+

Do not over-engineer the project.

---

# Technical Baseline

## Runtime

- Python 3
- Pygame
- Raspberry Pi 3B/3B+
- Linux
- Windows development environment

## Display

The game uses a fixed logical resolution:

    320 × 180 pixels

This is the game's internal coordinate system.

The logical framebuffer is scaled to the physical display.

Requirements:

- 16:9 aspect ratio
- Nearest-neighbor scaling
- No filtering
- No interpolation
- Pixel-art friendly
- Gameplay coordinates must always use logical 320×180 coordinates
- Physical monitor resolution must never affect gameplay calculations

The game should support fullscreen output at common resolutions such as
1280×720 and 1920×1080.

During development, windowed mode should be available.

---

# Performance

Target:

    60 FPS

The Raspberry Pi 3B/3B+ is the primary performance constraint.

Prefer straightforward implementations that perform well over clever or
complex architectures.

Avoid:

- Unnecessary per-frame object creation
- Unnecessary filesystem access during gameplay
- Excessive third-party dependencies
- Expensive operations inside the main loop
- Premature optimization

Measure before optimizing.

---

# Game Loop

Use a conventional game loop with frame-rate-independent gameplay.

Target approximately:

    60 updates/sec
    60 renders/sec

Do not make movement, timers, animation, or physics depend directly on the
number of frames rendered.

Use elapsed time/delta time where appropriate.

Keep update logic and rendering logically separated.

---

# Input

Create an input abstraction layer.

Game code should NOT directly depend on keyboard keys or raw controller
button numbers.

Support:

- USB game controllers through Pygame
- Keyboard controls for development

At minimum expose these logical actions:

    UP
    DOWN
    LEFT
    RIGHT
    A
    B
    START
    SELECT
    MENU

Controller mappings should be configurable.

Keyboard input should provide an equivalent development control scheme.

The game must remain playable if a controller is not connected.

---

# World

Use a tile-based 2D world.

Baseline tile size:

    16 × 16 pixels

Maps should be substantially larger than the visible screen.

World coordinates and screen coordinates must remain separate.

The camera converts world coordinates into screen coordinates.

---

# Tilemaps

Do not hard-code maps into Python source.

Maps must be external data.

Initially use a simple human-readable format such as JSON unless there is a
strong reason to use something else.

The architecture should allow eventual integration with a dedicated tilemap
editor.

Tilemaps should support at least:

- Background/ground tiles
- Solid collision tiles
- Decorative tiles
- Foreground tiles
- Objects
- Entities
- Spawn points
- Trigger regions

---

# Entities

Use simple Python classes for game entities.

Do NOT build a complicated ECS unless performance or project requirements
later demonstrate that it is necessary.

Entities may include:

- Player
- NPC
- Enemy
- Companion
- Item
- Interactive object
- Projectile
- Temporary effect

Entities should be able to have:

- Position
- Velocity
- Sprite
- Animation
- Collision properties
- Update behavior
- Render behavior

Keep visual representation separate from collision representation.

---

# Collision

Implement simple 2D collision appropriate for a top-down retro game.

Support:

- Solid world geometry
- Entity collision boxes
- Trigger regions
- Interaction regions

Sprite dimensions and collision dimensions must be independently configurable.

Do not assume the visible sprite is the collision box.

---

# Camera

Implement a reusable camera system.

The camera must:

- Follow the active player/entity
- Respect map boundaries
- Convert world coordinates to screen coordinates
- Support configurable smoothing or follow behavior
- Eventually support a configurable dead zone

The camera must not modify world coordinates.

---

# Sprites and Animation

Sprites are external PNG assets.

Support:

- Sprite sheets
- Individual sprite images
- Animation sequences
- Directional animations
- Configurable animation speed
- Sprite flipping where useful
- Nearest-neighbor rendering

Create reusable sprite/animation functionality.

Do not implement animation logic independently inside every character class.

All pixel art must remain crisp.

---

# UI

Create a lightweight UI system supporting:

- Text
- Dialogue boxes
- Menus
- HUD
- Pause screen
- Title screen

UI uses the same:

    320 × 180

logical coordinate system.

Do not use native OS UI elements.

---

# Fonts

Use external bitmap/pixel fonts.

Fonts should not be embedded directly into Python source.

---

# Audio

Support:

- Background music
- Sound effects
- Master volume
- Music volume
- SFX volume

Missing optional audio assets should fail gracefully rather than crashing
the game.

---

# Game States

Use a simple state machine.

At minimum support:

    BOOT
    TITLE
    GAMEPLAY
    PAUSE
    DIALOGUE
    GAME_OVER

States should be independently updateable/renderable and able to transition
cleanly.

Do not restart the entire application when changing states.

---

# Save System

Implement a simple save system.

Initially use JSON.

Save data should be capable of storing:

- Current map
- Player/world position
- Game progress flags
- Inventory
- Persistent game variables

Do not implement encryption or complicated serialization unless later
required.

---

# Data-Driven Design

Keep game-specific content separate from engine functionality.

Prefer configuration/data files for:

- Maps
- Dialogue
- Items
- NPC definitions
- Game settings
- Other content

Avoid hard-coding game content into engine systems.

---

# Project Structure

Use a structure approximately like:

    RetroGame/
    │
    ├── CLAUDE.md
    ├── README.md
    ├── requirements.txt
    ├── main.py
    │
    ├── engine/
    │   ├── game.py
    │   ├── input.py
    │   ├── renderer.py
    │   ├── camera.py
    │   ├── collision.py
    │   ├── entity.py
    │   ├── animation.py
    │   ├── tilemap.py
    │   ├── audio.py
    │   ├── state.py
    │   ├── save.py
    │   └── ui.py
    │
    ├── game/
    │   ├── player.py
    │   ├── npc.py
    │   ├── enemy.py
    │   └── interactions.py
    │
    ├── data/
    │   ├── maps/
    │   ├── dialogue/
    │   └── entities/
    │
    ├── assets/
    │   ├── sprites/
    │   ├── tiles/
    │   ├── fonts/
    │   ├── music/
    │   ├── sounds/
    │   └── ui/
    │
    └── tests/

This structure is a guideline, not an absolute requirement.

If a simpler structure is clearly better, use it.

---

# Architecture Rules

Follow these rules unless there is a compelling technical reason not to.

1. Prefer simple solutions.
2. Prefer readable code over clever code.
3. Avoid unnecessary abstractions.
4. Avoid unnecessary dependencies.
5. Keep engine code separate from game-specific code.
6. Keep game data separate from Python code.
7. Keep configuration values configurable.
8. Never hard-code the physical display resolution throughout the project.
9. Never hard-code controller button numbers throughout gameplay code.
10. Keep collision boxes independent of sprite dimensions.
11. Keep world coordinates independent of screen coordinates.
12. Keep rendering independent from game logic.
13. Avoid global mutable state where practical.
14. Do not add systems that the current milestone does not require.
15. Do not rewrite working systems unnecessarily.

---

# Development Workflow

The project is being developed interactively with an AI coding agent.

When asked to implement a feature:

1. Inspect the existing project before changing it.
2. Understand the existing architecture.
3. Reuse existing systems when possible.
4. Make the smallest reasonable change.
5. Run the relevant tests.
6. Run the game or an appropriate validation step when possible.
7. Fix errors discovered during validation.
8. Do not silently change unrelated systems.
9. Summarize what changed.

Do not assume a file or system exists without checking.

Do not create duplicate systems because an existing implementation was not
noticed.

---

# Testing

Create lightweight tests for important non-visual systems where practical.

Prioritize testing:

- Input abstraction
- Collision
- Camera calculations
- Animation state
- Game state transitions
- Save/load behavior
- Data loading

Visual/gameplay testing should be performed by actually running the game when
possible.

---

# Debugging

Provide a development/debug mode.

Useful debug information may include:

- FPS
- Player/world coordinates
- Current map
- Current game state
- Collision boxes
- Entity count

Debug rendering must be disabled in production mode.

---

# Configuration

Centralize important configuration values.

At minimum make these configurable:

- Logical resolution
- Target FPS
- Fullscreen/windowed mode
- Display scaling
- Controller mappings
- Audio volumes
- Debug mode

Do not scatter magic numbers throughout the code.

---

# Initial Milestone

The first milestone is ONLY a technical prototype.

Do not implement the final game's characters, story, mechanics, art direction,
or content yet.

The prototype must demonstrate:

1. 320×180 logical rendering
2. Window scaling
3. Keyboard input
4. USB controller input
5. A test tilemap larger than the screen
6. A controllable test entity
7. Solid tile collision
8. Camera following
9. Sprite-sheet animation
10. Basic sound playback
11. Pause state
12. Debug overlay
13. Clean project structure
14. Windows setup instructions
15. Raspberry Pi setup instructions

Placeholder graphics are completely acceptable.

Use simple generated/test graphics rather than spending time creating final
art assets.

---

# Milestone Procedure

Do not attempt to build the entire game at once.

For each milestone:

1. Define the smallest useful implementation.
2. Implement it.
3. Test it.
4. Run the game when appropriate.
5. Fix problems.
6. Stop when the milestone works.
7. Report the result.

At the end of a milestone, report:

- What was implemented
- Files created/modified
- How to run it
- Tests performed
- Any known problems
- Recommended next step

Do not automatically continue into unrelated features.

---

# Game-Specific Content

Game-specific design has intentionally NOT been defined here.

Do not invent:

- Characters
- Story
- Setting
- Enemies
- Items
- Quests
- Dialogue
- Combat mechanics
- Art direction
- Progression systems

Those will be provided separately.

When game-specific requirements are later provided, implement them using the
existing framework rather than contaminating generic engine systems with
game-specific assumptions.

---

# Current Priority

The immediate objective is:

BUILD THE SMALLEST CLEAN, PLAYABLE PYGAME PROTOTYPE THAT RUNS ON WINDOWS
AND CAN EVENTUALLY RUN ON A RASPBERRY PI 3B/3B+.

Favor working software over architectural perfection.

## Agent Behavior

You are authorized to create and modify project files and run development
commands necessary to complete the current task.

However:

- Do not install system-wide software without explicit approval.
- Do not modify files outside the project directory without explicit approval.
- Do not delete or overwrite user-created assets without explicit approval.
- Do not make major architectural changes without explaining them first.
- Do not proceed into a new milestone without being asked.
- When a decision could materially change the project's architecture or
  gameplay behavior, stop and ask for clarification.