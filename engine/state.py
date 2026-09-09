"""State machine with stack semantics for top-level game states.

At minimum the project supports BOOT, TITLE, GAMEPLAY, PAUSE, DIALOGUE,
and GAME_OVER states (see CLAUDE.md). This module only provides the
generic machinery; concrete states are registered by whoever owns the
StateMachine (see game/states.py).

Lifecycle rules:
- change(name): replaces the ENTIRE stack with a single state. Every
  state currently on the stack is exited (top to bottom), then the new
  state is entered. This is a full transition (e.g. TITLE -> GAMEPLAY,
  or leaving gameplay back to the title screen) - the state being left
  behind is genuinely torn down.
- push(name): suspends the current top state and places a new state on
  top of it. The suspended state's exit()/enter() are NOT called - it
  simply stops receiving update()/handle_input() until the state above
  it is popped. This is for overlays (pause, dialogue, menus) that must
  not reset whatever is underneath them.
- pop(): exits and removes the current top state, resuming whatever is
  beneath it exactly as it was left (no enter() call - it was never
  exited). No-op if the stack is empty.
- update()/handle_input(): only the top of the stack runs.
- render(): the WHOLE stack renders bottom-to-top, so a suspended state
  underneath an overlay (e.g. gameplay behind a pause screen) stays
  visible beneath it.
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
        self._stack = []

    def register(self, name, state):
        self._states[name] = state

    def get(self, name):
        return self._states.get(name)

    @property
    def current_name(self):
        return self._stack[-1] if self._stack else None

    @property
    def current_state(self):
        return self._states[self._stack[-1]] if self._stack else None

    def change(self, name, **kwargs):
        """Replace the entire stack with a single new state."""
        while self._stack:
            self._exit_top()
        self.push(name, **kwargs)

    def push(self, name, **kwargs):
        """Suspend the current top state (if any) and enter a new one on top."""
        self._stack.append(name)
        self._states[name].enter(**kwargs)

    def pop(self):
        """Exit and remove the current top state, resuming the one beneath it."""
        if self._stack:
            self._exit_top()

    def _exit_top(self):
        name = self._stack.pop()
        self._states[name].exit()

    def handle_input(self, input_manager):
        if self.current_state:
            self.current_state.handle_input(input_manager)

    def update(self, dt):
        if self.current_state:
            self.current_state.update(dt)

    def render(self, surface):
        for name in self._stack:
            self._states[name].render(surface)
