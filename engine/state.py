"""Minimal state machine for top-level game states.

At minimum the project supports BOOT, TITLE, GAMEPLAY, PAUSE, DIALOGUE,
and GAME_OVER states (see CLAUDE.md). This module only provides the
generic machinery; concrete states are registered by whoever owns the
StateMachine (see game/states.py).
"""


class State:
    def __init__(self, game):
        self.game = game

    def enter(self, **kwargs):
        pass

    def exit(self):
        pass

    def handle_input(self, input_manager):
        pass

    def update(self, dt):
        pass

    def render(self, surface):
        pass

    def debug_lines(self):
        """Optional extra lines shown in the debug overlay while this state is active."""
        return []


class StateMachine:
    def __init__(self):
        self._states = {}
        self.current_name = None
        self.current_state = None

    def register(self, name, state):
        self._states[name] = state

    def get(self, name):
        return self._states.get(name)

    def change(self, name, **kwargs):
        if self.current_state is not None:
            self.current_state.exit()
        self.current_name = name
        self.current_state = self._states[name]
        self.current_state.enter(**kwargs)

    def handle_input(self, input_manager):
        if self.current_state:
            self.current_state.handle_input(input_manager)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self, surface):
        if self.current_state:
            self.current_state.render(surface)
