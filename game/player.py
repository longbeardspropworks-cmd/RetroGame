"""Test/placeholder controllable entity.

This exists to validate the engine's input, movement, collision, camera,
and animation systems for the Initial Milestone. It is intentionally
generic (no character identity, story, or final art) - see CLAUDE.md's
"Game-Specific Content" section.
"""
from engine.entity import Entity
from engine.animation import SpriteSheet, Animation, Animator
from engine import collision

SPEED = 60.0  # logical pixels per second
FRAME_DURATION = 0.15
DIAGONAL_FACTOR = 0.7071  # 1/sqrt(2), so diagonal movement isn't faster

_spritesheet_cache = None


def _get_spritesheet():
    global _spritesheet_cache
    if _spritesheet_cache is None:
        _spritesheet_cache = SpriteSheet("assets/sprites/player.png", 16, 16)
    return _spritesheet_cache


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, collision_width=12, collision_height=12)
        self.sprite_offset_x = -2
        self.sprite_offset_y = -4
        self.facing = "down"

        sheet = _get_spritesheet()
        self.animator = Animator()
        # Sheet rows: 0=down, 1=up, 2=right (2 walk frames each). "left" is
        # derived by horizontally flipping "right" rather than drawing a
        # fourth row, to exercise the animator's sprite-flipping support.
        self.animator.add("down", Animation([sheet.get_frame(0, 0), sheet.get_frame(1, 0)], FRAME_DURATION))
        self.animator.add("up", Animation([sheet.get_frame(0, 1), sheet.get_frame(1, 1)], FRAME_DURATION))
        self.animator.add("right", Animation([sheet.get_frame(0, 2), sheet.get_frame(1, 2)], FRAME_DURATION))
        self.animator.play("down")

    def handle_input(self, input_manager):
        move_x = 0
        move_y = 0
        if input_manager.is_pressed("LEFT"):
            move_x -= 1
        if input_manager.is_pressed("RIGHT"):
            move_x += 1
        if input_manager.is_pressed("UP"):
            move_y -= 1
        if input_manager.is_pressed("DOWN"):
            move_y += 1

        if move_x != 0 and move_y != 0:
            move_x *= DIAGONAL_FACTOR
            move_y *= DIAGONAL_FACTOR

        self.vx = move_x * SPEED
        self.vy = move_y * SPEED

        if move_x < 0:
            self.facing = "left"
        elif move_x > 0:
            self.facing = "right"
        elif move_y < 0:
            self.facing = "up"
        elif move_y > 0:
            self.facing = "down"

    def update(self, dt, tilemap):
        moving = self.vx != 0 or self.vy != 0

        if self.facing == "left":
            self.animator.flip_x = True
            self.animator.play("right")
        else:
            self.animator.flip_x = False
            self.animator.play(self.facing)

        if moving:
            self.animator.update(dt)

        self.x, self.y = collision.move_with_tile_collision(
            self.x, self.y, self.collision_width, self.collision_height,
            self.vx * dt, self.vy * dt, tilemap)
