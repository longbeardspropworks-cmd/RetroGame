"""Generate placeholder tile assets for Alphabet Excavation.

Run once after installing dependencies, from the project root:
    python games/alphabet_excavation/tools/generate_assets.py

Tile 1 (dirt/unexcavated) is Level 1's starting ground; tile 2
(excavated, a darker brown) is what the dig mechanic swaps a cell to.
"""
import os

import pygame

TILE_SIZE = 16


def _ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def generate_tileset(path):
    surface = pygame.Surface((TILE_SIZE * 2, TILE_SIZE), pygame.SRCALPHA)

    # 1: dirt (unexcavated) - the letter mask before digging
    dirt = pygame.Surface((TILE_SIZE, TILE_SIZE))
    dirt.fill((120, 84, 52))
    pygame.draw.line(dirt, (98, 66, 40), (0, 5), (15, 5))
    pygame.draw.line(dirt, (98, 66, 40), (0, 11), (15, 11))
    surface.blit(dirt, (0, 0))

    # 2: excavated (open ground) - not used by Level 1 yet, placeholder
    # for the dig mechanic to swap into later.
    excavated = pygame.Surface((TILE_SIZE, TILE_SIZE))
    excavated.fill((60, 48, 36))
    surface.blit(excavated, (TILE_SIZE, 0))

    _ensure_dir(path)
    pygame.image.save(surface, path)
    print(f"wrote {path}")


def generate_excavator_sprite(path):
    """3 frames in a row: idle, and two alternating "digging" frames (a
    scoop mark that shifts up/down) for a simple back-and-forth digging
    animation. No directional/walk animation yet since footprint, speed,
    and movement model are all still undecided."""
    sheet = pygame.Surface((TILE_SIZE * 3, TILE_SIZE), pygame.SRCALPHA)
    body_color = (220, 170, 30)
    border_color = (90, 70, 10)
    scoop_color = (70, 50, 25)

    idle = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(idle, body_color, (1, 1, 14, 14))
    pygame.draw.rect(idle, border_color, (1, 1, 14, 14), 2)
    sheet.blit(idle, (0, 0))

    dig_a = idle.copy()
    pygame.draw.rect(dig_a, scoop_color, (5, 11, 6, 3))
    sheet.blit(dig_a, (TILE_SIZE, 0))

    dig_b = idle.copy()
    pygame.draw.rect(dig_b, scoop_color, (5, 9, 6, 5))
    sheet.blit(dig_b, (TILE_SIZE * 2, 0))

    _ensure_dir(path)
    pygame.image.save(sheet, path)
    print(f"wrote {path}")


def main():
    pygame.init()
    generate_tileset("games/alphabet_excavation/assets/tiles/tileset.png")
    generate_excavator_sprite("games/alphabet_excavation/assets/sprites/excavator.png")
    pygame.quit()


if __name__ == "__main__":
    main()
