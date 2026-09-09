"""Placeholder player/excavator entity for Alphabet Excavation.

Movement speed, collision footprint, and animation details are all still
placeholders (see games/alphabet_excavation/states.py), but digging now
does something: pressing A while standing on unexcavated dirt (ground
tile id DIRT_TILE_ID) starts a brief dig, during which the excavator
can't move and plays a "digging" animation; on completion the tile
underneath flips to the excavated id (a darker brown in the tileset).
"""
from engine.entity import Entity
from engine.animation import load_spritesheet, Animation, Animator

SPEED = 50.0  # placeholder logical pixels/sec - not finalized
DIAGONAL_FACTOR = 0.7071  # 1/sqrt(2), so diagonal movement isn't faster

DIRT_TILE_ID = 1
EXCAVATED_TILE_ID = 2
DIG_DURATION = 0.35  # seconds - placeholder


class Excavator(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, collision_width=10, collision_height=10)
        self.sprite_offset_x = -3
        self.sprite_offset_y = -3

        sheet = load_spritesheet("games/alphabet_excavation/assets/sprites/excavator.png", 16, 16)
        self.animator = Animator()
        self.animator.add("idle", Animation([sheet.get_frame(0, 0)], frame_duration=1.0))
        self.animator.add("digging", Animation([sheet.get_frame(1, 0), sheet.get_frame(2, 0)], frame_duration=0.12))
        self.animator.play("idle")

        self.is_digging = False
        self._dig_timer = 0.0
        self._dig_tile = None

    def handle_input(self, input_manager, tilemap):
        if self.is_digging:
            self.vx = 0.0
            self.vy = 0.0
            return

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

        if input_manager.is_just_pressed("A"):
            self._try_start_dig(tilemap)

    def update(self, dt, tilemap):
        if self.is_digging:
            self.animator.update(dt)
            self._dig_timer -= dt
            if self._dig_timer <= 0:
                self._finish_dig(tilemap)
            return

        self.animator.update(dt)
        self.move_with_collision(self.vx * dt, self.vy * dt, tilemap)

    def _try_start_dig(self, tilemap):
        tile_x, tile_y = tilemap.world_to_tile(
            self.x + self.collision_width / 2, self.y + self.collision_height / 2)
        if tilemap.get_ground_tile(tile_x, tile_y) != DIRT_TILE_ID:
            return  # nothing to dig here (already excavated, or outside the mask)

        self.is_digging = True
        self._dig_timer = DIG_DURATION
        self._dig_tile = (tile_x, tile_y)
        self.vx = 0.0
        self.vy = 0.0
        self.animator.play("digging", restart=True)

    def _finish_dig(self, tilemap):
        tile_x, tile_y = self._dig_tile
        tilemap.set_ground_tile(tile_x, tile_y, EXCAVATED_TILE_ID)
        self.is_digging = False
        self._dig_tile = None
        self.animator.play("idle")
