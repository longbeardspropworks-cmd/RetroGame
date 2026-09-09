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

    def test_push_does_not_exit_or_reenter_the_suspended_state(self):
        machine = StateMachine()
        base = RecordingState(None, "BASE")
        overlay = RecordingState(None, "OVERLAY")
        machine.register("BASE", base)
        machine.register("OVERLAY", overlay)

        machine.change("BASE")
        machine.push("OVERLAY")

        # BASE was never exited, and its enter() was not called again.
        self.assertEqual(base.events, [("enter", {})])
        self.assertEqual(overlay.events, [("enter", {})])
        self.assertEqual(machine.current_name, "OVERLAY")

    def test_pop_exits_top_and_resumes_state_beneath_without_reentering_it(self):
        machine = StateMachine()
        base = RecordingState(None, "BASE")
        overlay = RecordingState(None, "OVERLAY")
        machine.register("BASE", base)
        machine.register("OVERLAY", overlay)

        machine.change("BASE")
        machine.push("OVERLAY")
        machine.pop()

        self.assertEqual(overlay.events, [("enter", {}), ("exit", {})])
        # BASE is resumed with no further enter()/exit() calls of its own.
        self.assertEqual(base.events, [("enter", {})])
        self.assertEqual(machine.current_name, "BASE")

    def test_pop_on_empty_stack_is_a_no_op(self):
        machine = StateMachine()
        machine.pop()  # must not raise
        self.assertIsNone(machine.current_name)

    def test_update_and_input_only_reach_the_top_of_the_stack(self):
        machine = StateMachine()
        base = RecordingState(None, "BASE")
        overlay = RecordingState(None, "OVERLAY")
        machine.register("BASE", base)
        machine.register("OVERLAY", overlay)
        machine.change("BASE")
        machine.push("OVERLAY")

        machine.update(0.016)

        self.assertEqual(base.events, [("enter", {})])  # no ("update", ...) reached BASE
        self.assertEqual(overlay.events, [("enter", {}), ("update", 0.016)])

    def test_render_draws_the_whole_stack_bottom_to_top(self):
        machine = StateMachine()
        base = RecordingState(None, "BASE")
        overlay = RecordingState(None, "OVERLAY")
        machine.register("BASE", base)
        machine.register("OVERLAY", overlay)
        machine.change("BASE")
        machine.push("OVERLAY")

        machine.render("surface")

        self.assertIn(("render", "surface"), base.events)
        self.assertIn(("render", "surface"), overlay.events)

    def test_change_while_stack_has_an_overlay_unwinds_everything(self):
        machine = StateMachine()
        base = RecordingState(None, "BASE")
        overlay = RecordingState(None, "OVERLAY")
        other = RecordingState(None, "OTHER")
        machine.register("BASE", base)
        machine.register("OVERLAY", overlay)
        machine.register("OTHER", other)
        machine.change("BASE")
        machine.push("OVERLAY")

        machine.change("OTHER")

        self.assertEqual(base.events, [("enter", {}), ("exit", {})])
        self.assertEqual(overlay.events, [("enter", {}), ("exit", {})])
        self.assertEqual(other.events, [("enter", {})])
        self.assertEqual(machine.current_name, "OTHER")


if __name__ == "__main__":
    unittest.main()
