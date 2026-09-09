"""Sprite-sheet animation shared by all entities.

Centralizing frame timing/looping/flipping here means individual entity
classes just declare their animations and call play()/update() - they
don't reimplement animation bookkeeping themselves.
"""
import pygame


class SpriteSheet:
    def __init__(self, path, frame_width, frame_height):
        self.sheet = pygame.image.load(path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_frame(self, column, row):
        rect = pygame.Rect(column * self.frame_width, row * self.frame_height,
                            self.frame_width, self.frame_height)
        return self.sheet.subsurface(rect).copy()


class Animation:
    def __init__(self, frames, frame_duration, loop=True):
        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self._timer = 0.0
        self._index = 0

    def reset(self):
        self._timer = 0.0
        self._index = 0

    def update(self, dt):
        if len(self.frames) <= 1:
            return
        self._timer += dt
        while self._timer >= self.frame_duration:
            self._timer -= self.frame_duration
            self._index += 1
            if self._index >= len(self.frames):
                self._index = 0 if self.loop else len(self.frames) - 1

    def current_frame(self):
        return self.frames[self._index]


class Animator:
    """Holds a set of named animations and tracks which one is playing."""

    def __init__(self):
        self._animations = {}
        self._flipped_cache = {}
        self.current_name = None
        self.flip_x = False

    def add(self, name, animation):
        self._animations[name] = animation

    def play(self, name, restart=False):
        if name not in self._animations:
            raise KeyError(f"Unknown animation '{name}'")
        if self.current_name != name or restart:
            self.current_name = name
            self._animations[name].reset()

    def update(self, dt):
        if self.current_name is not None:
            self._animations[self.current_name].update(dt)

    def current_surface(self):
        frame = self._animations[self.current_name].current_frame()
        if not self.flip_x:
            return frame
        cache_key = (self.current_name, id(frame))
        flipped = self._flipped_cache.get(cache_key)
        if flipped is None:
            flipped = pygame.transform.flip(frame, True, False)
            self._flipped_cache[cache_key] = flipped
        return flipped
