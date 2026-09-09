"""Alphabet Excavation's game states.

LEVEL 1 - CAPITAL A
The level's tilemap (games/alphabet_excavation/data/levels/level_1_a.json)
IS the letter: its collision layer is solid everywhere outside the "A"
shape and open everywhere inside it, so the engine's existing tile
collision system already enforces "the excavator can never leave the
letter" with no new engine capability. Its ground layer holds the same
shape using a "dirt" tile id, giving the excavation-site look before any
digging happens.

Digging (A button) is implemented in games/alphabet_excavation/excavator.py.
Level completion (every dirt cell excavated) is detected below and shown
with a simple banner - no progression to a next level yet.

Deliberately NOT implemented yet - this is scaffolding only:
- Any tuning of excavator footprint, speed, dig duration, or animation.
- Any state other than this one (no title/menu/progression yet).
"""
import pygame

from engine.state import State
from engine.tilemap import TileMap
from engine.camera import Camera
from engine.ui import TextRenderer
from games.alphabet_excavation.excavator import Excavator, DIRT_TILE_ID

LEVEL_1_PATH = "games/alphabet_excavation/data/levels/level_1_a.json"

_text = TextRenderer()


class Level1State(State):
    def enter(self):
        self.tilemap = TileMap.load(LEVEL_1_PATH)
        spawn = self.tilemap.spawn_points[0] if self.tilemap.spawn_points else {"x": 0, "y": 0}
        self.excavator = Excavator(spawn["x"], spawn["y"])
        self.entities = [self.excavator]

        self.camera = Camera(self.game.renderer.logical_width, self.game.renderer.logical_height)
        self.camera.set_world_bounds(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.camera.follow(self.excavator.x, self.excavator.y, smoothing=1.0)

        self.is_complete = False

    def handle_input(self, input_manager):
        self.excavator.handle_input(input_manager, self.tilemap)

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt, self.tilemap)
        self.camera.follow(
            self.excavator.x + self.excavator.collision_width / 2,
            self.excavator.y + self.excavator.collision_height / 2,
            smoothing=0.15,
        )

        if not self.is_complete and self._is_fully_excavated():
            self.is_complete = True

    def _is_fully_excavated(self):
        return not any(tile_id == DIRT_TILE_ID for row in self.tilemap.ground for tile_id in row)

    def render(self, surface):
        surface.fill((20, 16, 12))
        self.tilemap.render_ground(surface, self.camera)

        for entity in sorted(self.entities, key=lambda e: e.y + e.collision_height):
            entity.render(surface, self.camera)

        if self.game.debug:
            self._render_collision_boxes(surface)

        if self.is_complete:
            self._render_complete_banner(surface)

    def _render_collision_boxes(self, surface):
        for entity in self.entities:
            rect = entity.get_collision_rect()
            screen_x, screen_y = self.camera.world_to_screen(rect.x, rect.y)
            debug_rect = pygame.Rect(round(screen_x), round(screen_y), rect.width, rect.height)
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)

    def _render_complete_banner(self, surface):
        overlay = surface.copy()
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120)
        surface.blit(overlay, (0, 0))
        _text.draw(surface, "LEVEL COMPLETE!", 108, 75, color=(255, 255, 255))
        _text.draw(surface, "YOU DUG OUT THE LETTER A", 68, 95, color=(255, 220, 120))

    def debug_lines(self):
        return [
            "LEVEL: Capital A",
            f"POS: {self.excavator.x:.1f}, {self.excavator.y:.1f}",
            f"DIGGING: {self.excavator.is_digging}",
            f"COMPLETE: {self.is_complete}",
        ]
