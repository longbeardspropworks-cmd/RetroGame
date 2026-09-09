"""Lightweight UI/text helpers.

NOTE: this prototype renders text with pygame's built-in font as a
placeholder. CLAUDE.md's Fonts section calls for external bitmap/pixel
fonts; swapping in a real bitmap font later only requires changing this
module, not any calling code (game/states.py and engine/game.py only
call TextRenderer.draw()).
"""
import pygame


class TextRenderer:
    def __init__(self, size=8):
        pygame.font.init()
        self._font = pygame.font.SysFont("consolas,couriernew,monospace", size)

    def draw(self, surface, text, x, y, color=(255, 255, 255)):
        image = self._font.render(text, False, color)
        surface.blit(image, (x, y))
