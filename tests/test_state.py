import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.state import State, StateMachine


class RecordingState(State):
    def __init__(self, game, name):
        super().__init__(game)
        self.name = name
        self.events = []

    def enter(self, **kwargs):
        self.events.append(("enter", kwargs))

    def exit(self):
        self.events.append(("exit", {}))

    def update(self, dt):
        self.events.append(("update", dt))

    def render(self, surface):
        self.events.append(("render", surface))


class StateMachineTests(unittest.TestCase):
    def test_change_calls_enter_on_new_state(self):
        machine = StateMachine()
        state_a = RecordingState(None, "A")
        machine.register("A", state_a)
        machine.change("A", foo="bar")
        self.assertEqual(machine.current_name, "A")
        self.assertEqual(state_a.events, [("enter", {"foo": "bar"})])

    def test_change_calls_exit_on_previous_state(self):
        machine = StateMachine()
        state_a = RecordingState(None, "A")
        state_b = RecordingState(None, "B")
        machine.register("A", state_a)
        machine.register("B", state_b)

        machine.change("A")
        machine.change("B")

        self.assertEqual(state_a.events, [("enter", {}), ("exit", {})])
        self.assertEqual(state_b.events, [("enter", {})])

    def test_update_and_render_delegate_to_current_state_only(self):
        machine = StateMachine()
        state_a = RecordingState(None, "A")
        state_b = RecordingState(None, "B")
        machine.register("A", state_a)
        machine.register("B", state_b)
        machine.change("A")

        machine.update(0.016)
        machine.render("surface")

        self.assertEqual(state_a.events, [("enter", {}), ("update", 0.016), ("render", "surface")])
        self.assertEqual(state_b.events, [])

    def test_get_returns_registered_state(self):
        machine = StateMachine()
        state_a = RecordingState(None, "A")
        machine.register("A", state_a)
        self.assertIs(machine.get("A"), state_a)
        self.assertIsNone(machine.get("missing"))

    def test_update_before_any_change_does_not_crash(self):
        machine = StateMachine()
        machine.update(0.016)
        machine.render("surface")


if __name__ == "__main__":
    unittest.main()
