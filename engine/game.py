"""Top-level Game object: owns the window, engine systems, the state
machine, and the fixed-timestep main loop."""
import pygame

from engine.config import load_settings
from engine.renderer import Renderer
from engine.input import InputManager
from engine.audio import AudioManager
from engine.state import StateMachine
from engine.ui import TextRenderer

FIXED_DT = 1.0 / 60.0
MAX_FRAME_TIME = 0.25  # clamp long stalls so update() doesn't spiral


class Game:
    def __init__(self, register_states, settings_path="data/settings.json"):
        """`register_states` is called once with this Game instance and is
        responsible for registering every state the game needs on
        self.state_machine and setting the initial state (typically via
        state_machine.change(...)). Which states exist, and which one runs
        first, is entirely game-specific - the engine has no opinion on it,
        so any game can plug in its own state set without touching engine
        code (see games/prototype/main.py and games/alphabet_excavation/main.py
        for the two current examples).
        """
        self.settings = load_settings(settings_path)
        pygame.init()

        self.renderer = Renderer(self.settings["display"])
        self.input_manager = InputManager(self.settings["controls"])
        self.audio = AudioManager(self.settings["audio"])
        self.debug = self.settings.get("debug", False)

        self.state_machine = StateMachine()
        register_states(self)

        self._debug_text = TextRenderer()
        self.running = True

    def run(self):
        clock = pygame.time.Clock()
        accumulator = 0.0

        while self.running:
            frame_time = min(clock.tick(self.settings["fps"]) / 1000.0, MAX_FRAME_TIME)

            self._handle_events()
            self.input_manager.update()
            self.state_machine.handle_input(self.input_manager)

            accumulator += frame_time
            while accumulator >= FIXED_DT:
                self.state_machine.update(FIXED_DT)
                accumulator -= FIXED_DT

            self.renderer.begin_frame()
            self.state_machine.render(self.renderer.logical_surface)
            if self.debug:
                self._render_debug_overlay(clock)
            self.renderer.present()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.renderer.handle_resize()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    self.debug = not self.debug
                elif event.key == pygame.K_F11:
                    self.renderer.toggle_fullscreen()
            elif event.type in (pygame.JOYDEVICEADDED, pygame.JOYDEVICEREMOVED):
                self.input_manager.refresh_joystick()

    def _render_debug_overlay(self, clock):
        lines = [f"FPS: {clock.get_fps():.0f}", f"STATE: {self.state_machine.current_name}"]
        if self.state_machine.current_state is not None:
            lines.extend(self.state_machine.current_state.debug_lines())
        for i, line in enumerate(lines):
            self._debug_text.draw(self.renderer.logical_surface, line, 2, 2 + i * 8, color=(255, 255, 0))
