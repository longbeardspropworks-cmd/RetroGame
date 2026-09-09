"""Generate placeholder tile assets for Alphabet Excavation.

Run once after installing dependencies, from the project root:
    python games/alphabet_excavation/tools/generate_assets.py

Tile 1 (dirt/unexcavated) is the only one currently used by Level 1's
ground layer. Tile 2 (excavated/open ground) is generated now so the dig
mechanic can swap ground-layer cells from id 1 to id 2 later without
needing a new asset - see the Level 1 state's "what's deferred" notes.
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
    """Single static placeholder frame - no directional/walk animation yet
    since footprint, speed, and animation are all still undecided."""
    sheet = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.rect(sheet, (220, 170, 30), (1, 1, 14, 14))
    pygame.draw.rect(sheet, (90, 70, 10), (1, 1, 14, 14), 2)

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
