"""Base class for objects that live in the game world.

The visible sprite is deliberately kept separate from the collision box:
sprite_offset_x/y lets a sprite's pixels be aligned over a hitbox of a
different size, since the visible sprite should never be assumed to be
the collision box.
"""
import pygame


class Entity:
    def __init__(self, x, y, collision_width, collision_height):
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

    def update(self, dt):
        pass

    def render(self, surface, camera):
        if self.animator is None:
            return
        frame = self.animator.current_surface()
        screen_x, screen_y = camera.world_to_screen(
            self.x + self.sprite_offset_x, self.y + self.sprite_offset_y)
        surface.blit(frame, (round(screen_x), round(screen_y)))
