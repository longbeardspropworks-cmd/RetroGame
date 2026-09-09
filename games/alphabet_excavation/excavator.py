"""Placeholder player/excavator entity for Alphabet Excavation.

Movement speed, collision footprint, and digging behavior are all
explicitly unresolved right now (see games/alphabet_excavation/states.py).
This exists only to prove an entity can move around inside the
letter-shaped tilemap using the engine's existing input, collision,
animation, and asset-cache systems. The A button ("dig") is not wired
up to anything yet.
"""
from engine.entity import Entity
from engine.animation import load_spritesheet, Animation, Animator

SPEED = 50.0  # placeholder logical pixels/sec - not finalized
DIAGONAL_FACTOR = 0.7071  # 1/sqrt(2), so diagonal movement isn't faster


class Excavator(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, collision_width=10, collision_height=10)
        self.sprite_offset_x = -3
        self.sprite_offset_y = -3

        # Single static frame for now - no facing/walk animation until the
        # movement model and visual style are decided.
        sheet = load_spritesheet("games/alphabet_excavation/assets/sprites/excavator.png", 16, 16)
        self.animator = Animator()
        self.animator.add("idle", Animation([sheet.get_frame(0, 0)], frame_duration=1.0))
        self.animator.play("idle")

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

        # Digging (A button) intentionally does nothing yet.

    def update(self, dt, tilemap):
        self.move_with_collision(self.vx * dt, self.vy * dt, tilemap)
