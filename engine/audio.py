"""Audio playback with graceful handling of missing/optional assets.

Nothing here raises if the mixer fails to initialize or a sound/music
file is missing - it logs a warning and audio simply stays silent so a
missing asset never crashes the game.
"""
import pygame


class AudioManager:
    def __init__(self, audio_config):
        self._master_volume = audio_config.get("master_volume", 1.0)
        self._music_volume = audio_config.get("music_volume", 1.0)
        self._sfx_volume = audio_config.get("sfx_volume", 1.0)
        self._sounds = {}
        self._enabled = True
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"[audio] mixer unavailable, audio disabled: {e}")
            self._enabled = False

    def load_sound(self, name, path):
        if not self._enabled:
            return
        try:
            sound = pygame.mixer.Sound(path)
            sound.set_volume(self._sfx_volume * self._master_volume)
            self._sounds[name] = sound
        except (pygame.error, FileNotFoundError) as e:
            print(f"[audio] could not load sound '{name}' from {path}: {e}")

    def play_sound(self, name):
        if not self._enabled:
            return
        sound = self._sounds.get(name)
        if sound is not None:
            sound.play()

    def play_music(self, path, loop=True):
        if not self._enabled:
            return
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self._music_volume * self._master_volume)
            pygame.mixer.music.play(-1 if loop else 0)
        except (pygame.error, FileNotFoundError) as e:
            print(f"[audio] could not play music from {path}: {e}")

    def stop_music(self):
        if self._enabled:
            pygame.mixer.music.stop()

    def set_master_volume(self, value):
        self._master_volume = value
        self._apply_volumes()

    def set_music_volume(self, value):
        self._music_volume = value
        self._apply_volumes()

    def set_sfx_volume(self, value):
        self._sfx_volume = value
        self._apply_volumes()

    def _apply_volumes(self):
        if not self._enabled:
            return
        pygame.mixer.music.set_volume(self._music_volume * self._master_volume)
        for sound in self._sounds.values():
            sound.set_volume(self._sfx_volume * self._master_volume)
