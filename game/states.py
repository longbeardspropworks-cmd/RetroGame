"""Concrete top-level game states.

These compose reusable engine systems (tilemap, camera, collision) with
this project's placeholder test content (the test map and Player). They
live under game/, not engine/, because they reference specific data
paths and the Player class - engine/ stays free of project assumptions.
"""
import pygame

from engine.state import State
from engine.tilemap import TileMap
from engine.camera import Camera
from engine.ui import TextRenderer
from game.player import Player

TEST_MAP_PATH = "data/maps/test_map.json"

_text = TextRenderer()


class BootState(State):
    """Nothing to load yet, so this just advances straight to the title screen."""

    def enter(self):
        self._advanced = False

    def update(self, dt):
        if not self._advanced:
            self._advanced = True
            self.game.state_machine.change("TITLE")


class TitleState(State):
    def enter(self):
        self._blink_timer = 0.0
        self._show_prompt = True

    def handle_input(self, input_manager):
        if input_manager.is_just_pressed("START") or input_manager.is_just_pressed("A"):
            self.game.state_machine.change("GAMEPLAY")

    def update(self, dt):
        self._blink_timer += dt
        if self._blink_timer >= 0.5:
            self._blink_timer = 0.0
            self._show_prompt = not self._show_prompt

    def render(self, surface):
        surface.fill((20, 24, 36))
        _text.draw(surface, "RETRO GAME PROTOTYPE", 60, 70)
        if self._show_prompt:
            _text.draw(surface, "PRESS START", 120, 100)


class GameplayState(State):
    def __init__(self, game):
        super().__init__(game)
        self._initialized = False

    def enter(self):
        # Entering GAMEPLAY also happens when resuming from PAUSE, which
        # must not rebuild the world or reload assets from disk - only the
        # first entry (from TITLE) does full setup.
        if not self._initialized:
            self.tilemap = TileMap.load(TEST_MAP_PATH)
            spawn = self.tilemap.spawn_points[0] if self.tilemap.spawn_points else {"x": 32, "y": 32}
            self.player = Player(spawn["x"], spawn["y"])
            self.camera = Camera(self.game.renderer.logical_width, self.game.renderer.logical_height)
            self.camera.set_world_bounds(self.tilemap.pixel_width, self.tilemap.pixel_height)
            self.camera.follow(self.player.x, self.player.y, smoothing=1.0)
            self.game.audio.load_sound("beep", "assets/sounds/beep.wav")
            self._initialized = True

        self.game.audio.play_music("assets/music/placeholder_loop.wav")

    def exit(self):
        self.game.audio.stop_music()

    def handle_input(self, input_manager):
        if input_manager.is_just_pressed("START") or input_manager.is_just_pressed("MENU"):
            self.game.state_machine.change("PAUSE", previous="GAMEPLAY")
            return
        if input_manager.is_just_pressed("A"):
            self.game.audio.play_sound("beep")
        self.player.handle_input(input_manager)

    def update(self, dt):
        self.player.update(dt, self.tilemap)
        self.camera.follow(
            self.player.x + self.player.collision_width / 2,
            self.player.y + self.player.collision_height / 2,
            smoothing=0.15,
        )

    def render(self, surface):
        surface.fill((10, 10, 10))
        self.tilemap.render_ground(surface, self.camera)
        self.tilemap.render_decoration(surface, self.camera)
        self.player.render(surface, self.camera)
        self.tilemap.render_foreground(surface, self.camera)

        if self.game.debug:
            self._render_collision_boxes(surface)

    def _render_collision_boxes(self, surface):
        player_rect = self.player.get_collision_rect()
        screen_x, screen_y = self.camera.world_to_screen(player_rect.x, player_rect.y)
        debug_rect = pygame.Rect(round(screen_x), round(screen_y), player_rect.width, player_rect.height)
        pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)

    def debug_lines(self):
        return [
            f"MAP: {TEST_MAP_PATH}",
            f"POS: {self.player.x:.1f}, {self.player.y:.1f}",
            f"ENTITIES: 1",
        ]


class PauseState(State):
    def enter(self, previous="GAMEPLAY"):
        self._previous = previous

    def handle_input(self, input_manager):
        if input_manager.is_just_pressed("START") or input_manager.is_just_pressed("MENU"):
            self.game.state_machine.change(self._previous)

    def render(self, surface):
        self.game.state_machine.get(self._previous).render(surface)
        overlay = surface.copy()
        overlay.fill((0, 0, 0))
        overlay.set_alpha(140)
        surface.blit(overlay, (0, 0))
        _text.draw(surface, "PAUSED", 130, 85)
