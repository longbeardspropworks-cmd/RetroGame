"""Generate placeholder art/audio assets for the technical prototype.

Run once after installing dependencies:
    python tools/generate_assets.py

These are intentionally crude placeholder graphics/sounds (see the
"Initial Milestone" section of CLAUDE.md - placeholder graphics are
acceptable, final art comes later). Replace the files under assets/
with real art/audio later without touching any engine or game code.
"""
import math
import os
import struct
import wave

import pygame

TILE_SIZE = 16


def _ensure_dir(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def generate_tileset(path):
    """4 tiles left to right: grass (ground), wall (solid), flower
    (decoration), tree canopy (foreground, semi-transparent)."""
    surface = pygame.Surface((TILE_SIZE * 4, TILE_SIZE), pygame.SRCALPHA)

    grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
    grass.fill((58, 124, 58))
    pygame.draw.line(grass, (46, 102, 46), (0, 4), (15, 4))
    pygame.draw.line(grass, (46, 102, 46), (0, 11), (15, 11))
    surface.blit(grass, (0, 0))

    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall.fill((92, 84, 76))
    pygame.draw.rect(wall, (60, 54, 48), wall.get_rect(), 2)
    surface.blit(wall, (TILE_SIZE, 0))

    flower = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(flower, (220, 210, 90), (8, 8), 3)
    surface.blit(flower, (TILE_SIZE * 2, 0))

    canopy = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    pygame.draw.circle(canopy, (30, 90, 40, 220), (8, 8), 8)
    surface.blit(canopy, (TILE_SIZE * 3, 0))

    _ensure_dir(path)
    pygame.image.save(surface, path)
    print(f"wrote {path}")


def generate_player_sheet(path):
    """3 rows (down, up, right) x 2 walk frames, 16x16 each. "left" is
    derived at runtime by flipping "right" (see game/player.py)."""
    sheet = pygame.Surface((TILE_SIZE * 2, TILE_SIZE * 3), pygame.SRCALPHA)
    body_color = (70, 130, 200)
    face_color = (30, 60, 110)

    face_offset_by_row = {
        0: (7, 12),  # down: face mark near bottom
        1: (7, 2),   # up: face mark near top
        2: (12, 7),  # right: face mark near right edge
    }

    for row, (fx, fy) in face_offset_by_row.items():
        for col in range(2):
            frame = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            bob = 1 if col == 1 else 0
            pygame.draw.rect(frame, body_color, (2, 1 + bob, 12, 14 - bob))
            pygame.draw.rect(frame, face_color, (fx - 1, fy - 1, 3, 3))
            sheet.blit(frame, (col * TILE_SIZE, row * TILE_SIZE))

    _ensure_dir(path)
    pygame.image.save(sheet, path)
    print(f"wrote {path}")


def _write_wav(path, samples, sample_rate=22050):
    _ensure_dir(path)
    with wave.open(path, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(b"".join(struct.pack("<h", s) for s in samples))
    print(f"wrote {path}")


def generate_beep(path, frequency=880.0, duration=0.12, sample_rate=22050):
    sample_count = int(sample_rate * duration)
    samples = []
    for i in range(sample_count):
        t = i / sample_rate
        fade = min(1.0, min(i, sample_count - i) / (sample_rate * 0.02))
        samples.append(int(math.sin(2 * math.pi * frequency * t) * fade * 12000))
    _write_wav(path, samples, sample_rate)


def generate_music_loop(path, sample_rate=22050):
    """A short arpeggio loop - just enough to prove music playback works."""
    notes = [261.63, 329.63, 392.00, 523.25]  # C4 E4 G4 C5
    note_duration = 0.25
    samples = []
    for frequency in notes:
        count = int(sample_rate * note_duration)
        for i in range(count):
            t = i / sample_rate
            fade = min(1.0, min(i, count - i) / (sample_rate * 0.02))
            samples.append(int(math.sin(2 * math.pi * frequency * t) * fade * 9000))
    _write_wav(path, samples, sample_rate)


def main():
    pygame.init()
    generate_tileset("assets/tiles/tileset.png")
    generate_player_sheet("assets/sprites/player.png")
    generate_beep("assets/sounds/beep.wav")
    generate_music_loop("assets/music/placeholder_loop.wav")
    pygame.quit()


if __name__ == "__main__":
    main()
