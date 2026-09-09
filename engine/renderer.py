"""Logical-resolution rendering with integer nearest-neighbor scale-up.

Game code always draws onto a fixed 320x180 logical surface. The renderer
scales that surface up to fill the physical window using integer,
non-interpolated scaling, so pixel art stays crisp and gameplay math never
needs to know about the physical display resolution.
"""
import pygame


class Renderer:
    def __init__(self, display_config):
        self.logical_width = display_config["logical_width"]
        self.logical_height = display_config["logical_height"]
        self._windowed_size = (display_config["window_width"], display_config["window_height"])
        self._fullscreen = display_config["fullscreen"]

        if self._fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self._windowed_size, pygame.RESIZABLE)

        pygame.display.set_caption("Retro Game Prototype")
        self.logical_surface = pygame.Surface((self.logical_width, self.logical_height)).convert()

        self._scale = 1
        self._offset = (0, 0)
        self._recompute_scale()

    def _recompute_scale(self):
        window_width, window_height = self.window.get_size()
        scale = max(1, min(window_width // self.logical_width, window_height // self.logical_height))
        self._scale = scale
        scaled_width = self.logical_width * scale
        scaled_height = self.logical_height * scale
        self._offset = ((window_width - scaled_width) // 2, (window_height - scaled_height) // 2)

    def handle_resize(self):
        self._recompute_scale()

    def toggle_fullscreen(self):
        self._fullscreen = not self._fullscreen
        if self._fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(self._windowed_size, pygame.RESIZABLE)
        self._recompute_scale()

    def begin_frame(self, clear_color=(0, 0, 0)):
        self.logical_surface.fill(clear_color)

    def present(self):
        self.window.fill((0, 0, 0))
        scaled_size = (self.logical_width * self._scale, self.logical_height * self._scale)
        scaled_surface = pygame.transform.scale(self.logical_surface, scaled_size)
        self.window.blit(scaled_surface, self._offset)
        pygame.display.flip()
