import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

from engine.animation import Animation, Animator


class AnimationTests(unittest.TestCase):
    def test_advances_frames_over_time(self):
        anim = Animation(frames=["a", "b", "c"], frame_duration=0.1)
        self.assertEqual(anim.current_frame(), "a")
        anim.update(0.1)
        self.assertEqual(anim.current_frame(), "b")
        anim.update(0.1)
        self.assertEqual(anim.current_frame(), "c")

    def test_loops_back_to_first_frame(self):
        anim = Animation(frames=["a", "b"], frame_duration=0.1, loop=True)
        anim.update(0.25)  # advances two frames' worth of time
        self.assertEqual(anim.current_frame(), "a")

    def test_non_looping_animation_holds_last_frame(self):
        anim = Animation(frames=["a", "b"], frame_duration=0.1, loop=False)
        anim.update(1.0)
        self.assertEqual(anim.current_frame(), "b")

    def test_reset_returns_to_first_frame(self):
        anim = Animation(frames=["a", "b"], frame_duration=0.1)
        anim.update(0.1)
        self.assertEqual(anim.current_frame(), "b")
        anim.reset()
        self.assertEqual(anim.current_frame(), "a")

    def test_frame_independent_of_render_rate(self):
        # Advancing by many small dt steps should match one big step, as
        # long as the total isn't sitting exactly on a frame-duration
        # boundary (where float rounding could go either way).
        anim_small_steps = Animation(frames=["a", "b", "c"], frame_duration=0.1)
        anim_big_step = Animation(frames=["a", "b", "c"], frame_duration=0.1)
        for _ in range(21):
            anim_small_steps.update(0.01)
        anim_big_step.update(0.21)
        self.assertEqual(anim_small_steps.current_frame(), anim_big_step.current_frame())


class AnimatorTests(unittest.TestCase):
    def test_play_switches_current_animation(self):
        animator = Animator()
        animator.add("idle", Animation(["a"], 0.1))
        animator.add("walk", Animation(["x", "y"], 0.1))
        animator.play("idle")
        self.assertEqual(animator.current_surface(), "a")
        animator.play("walk")
        self.assertEqual(animator.current_surface(), "x")

    def test_playing_same_animation_again_does_not_reset_progress(self):
        animator = Animator()
        animator.add("walk", Animation(["x", "y"], 0.1))
        animator.play("walk")
        animator.update(0.1)
        self.assertEqual(animator.current_surface(), "y")
        animator.play("walk")  # same name again, should not reset
        self.assertEqual(animator.current_surface(), "y")

    def test_restart_flag_forces_reset(self):
        animator = Animator()
        animator.add("walk", Animation(["x", "y"], 0.1))
        animator.play("walk")
        animator.update(0.1)
        animator.play("walk", restart=True)
        self.assertEqual(animator.current_surface(), "x")

    def test_unknown_animation_raises(self):
        animator = Animator()
        with self.assertRaises(KeyError):
            animator.play("missing")


if __name__ == "__main__":
    unittest.main()
