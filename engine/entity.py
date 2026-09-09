"""Base class for objects that live in the game world.

This is deliberately minimal: position, optional update/render behavior,
and an optional collision box - not a "god class". Concrete entities
(Player, and later NPCs/enemies/items) override only what they need;
collision_width/height default to zero so a purely visual entity isn't
forced to define a meaningless hitbox.

The visible sprite is kept separate from the collision box: sprite_offset_x/y
lets a sprite's pixels be aligned over a hitbox of a different size, since
the visible sprite should never be assumed to be the collision box.
"""
import pygame

from engine import collision


class Entity:
    def __init__(self, x, y, collision_width=0, collision_height=0):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.collision_width = collision_width
        self.collision_height = collision_height
        self.sprite_offset_x = 0
        self.sprite_offset_y = 0
        self.animator = None

    def get_collision_rect(self):
        return pygame.Rect(int(round(self.x)), int(round(self.y)),
                            self.collision_width, self.collision_height)

    def move_with_collision(self, dx, dy, tilemap):
        """Move by (dx, dy), resolved against the tilemap's solid tiles.

        Optional convenience for entities that want tile collision (the
        Player uses this); an entity that doesn't move, or that moves
        without colliding with the map, simply doesn't call it.
        """
        self.x, self.y = collision.move_with_tile_collision(
            self.x, self.y, self.collision_width, self.collision_height, dx, dy, tilemap)

    def update(self, dt, tilemap=None):
        pass

    def render(self, surface, camera):
        if self.animator is None:
            return
        frame = self.animator.current_surface()
        screen_x, screen_y = camera.world_to_screen(
            self.x + self.sprite_offset_x, self.y + self.sprite_offset_y)
        surface.blit(frame, (round(screen_x), round(screen_y)))
