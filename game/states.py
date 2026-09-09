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
    """Owns a generic list of entities plus a named `player` reference into
    that same list. Update/render/debug-draw all iterate `self.entities`
    rather than special-casing the player, so adding an NPC/enemy/item
    later means appending to the list, not rewriting this state. Systems
    that legitimately need "the player" specifically (camera follow,
    input handling) use self.player directly.
    """

    def enter(self):
        self.tilemap = TileMap.load(TEST_MAP_PATH)
        spawn = self.tilemap.spawn_points[0] if self.tilemap.spawn_points else {"x": 32, "y": 32}
        self.player = Player(spawn["x"], spawn["y"])
        self.entities = [self.player]

        self.camera = Camera(self.game.renderer.logical_width, self.game.renderer.logical_height)
        self.camera.set_world_bounds(self.tilemap.pixel_width, self.tilemap.pixel_height)
        self.camera.follow(self.player.x, self.player.y, smoothing=1.0)

        self.game.audio.load_sound("beep", "assets/sounds/beep.wav")
        self.game.audio.play_music("assets/music/placeholder_loop.wav")

    def exit(self):
        self.game.audio.stop_music()

    def handle_input(self, input_manager):
        if input_manager.is_just_pressed("START") or input_manager.is_just_pressed("MENU"):
            self.game.state_machine.push("PAUSE")
            return
        if input_manager.is_just_pressed("A"):
            self.game.audio.play_sound("beep")
        self.player.handle_input(input_manager)

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt, self.tilemap)
        self.camera.follow(
            self.player.x + self.player.collision_width / 2,
            self.player.y + self.player.collision_height / 2,
            smoothing=0.15,
        )

    def render(self, surface):
        surface.fill((10, 10, 10))
        self.tilemap.render_ground(surface, self.camera)
        self.tilemap.render_decoration(surface, self.camera)

        # Y-sorted so an entity nearer the bottom of the screen (larger
        # world y) draws in front of one further up, as expected for a
        # top-down view.
        for entity in sorted(self.entities, key=lambda e: e.y + e.collision_height):
            entity.render(surface, self.camera)

        self.tilemap.render_foreground(surface, self.camera)

        if self.game.debug:
            self._render_collision_boxes(surface)

    def _render_collision_boxes(self, surface):
        for entity in self.entities:
            rect = entity.get_collision_rect()
            screen_x, screen_y = self.camera.world_to_screen(rect.x, rect.y)
            debug_rect = pygame.Rect(round(screen_x), round(screen_y), rect.width, rect.height)
            pygame.draw.rect(surface, (255, 0, 0), debug_rect, 1)

    def debug_lines(self):
        return [
            f"MAP: {TEST_MAP_PATH}",
            f"POS: {self.player.x:.1f}, {self.player.y:.1f}",
            f"ENTITIES: {len(self.entities)}",
        ]


class PauseState(State):
    """A pushed overlay: whatever state is beneath it on the stack (normally
    GAMEPLAY) keeps rendering underneath automatically - see
    StateMachine.render() - so this only needs to draw its own overlay."""

    def enter(self):
        self.game.audio.pause_music()

    def exit(self):
        self.game.audio.resume_music()

    def handle_input(self, input_manager):
        if input_manager.is_just_pressed("START") or input_manager.is_just_pressed("MENU"):
            self.game.state_machine.pop()

    def render(self, surface):
        overlay = surface.copy()
        overlay.fill((0, 0, 0))
        overlay.set_alpha(140)
        surface.blit(overlay, (0, 0))
        _text.draw(surface, "PAUSED", 130, 85)
