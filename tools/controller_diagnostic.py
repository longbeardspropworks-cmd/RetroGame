"""Controller diagnostic tool - a dev utility, NOT part of the game itself.

Lists every joystick/controller pygame detects, then shows live
button/axis/hat input as you press things, so you can read off the exact
numbers pygame reports for THIS controller and put them into
data/settings.json's `controls.controller` map.

This does not read or touch engine/input.py or the game's input mapping
at all - it only talks to pygame's raw joystick API directly, so it is
safe to run without affecting existing input behavior.

Run from the project root (with the venv activated):
    python tools/controller_diagnostic.py

Keep this around for whenever a new/different controller needs mapping.
"""
import sys

import pygame

WINDOW_SIZE = (640, 480)
LINE_HEIGHT = 18
AXIS_PRINT_DEADZONE = 0.15  # avoid flooding the console with idle stick drift


def describe_joystick(joystick):
    return [
        f"Name: {joystick.get_name()}",
        f"Instance ID: {joystick.get_instance_id()}",
        f"Buttons: {joystick.get_numbuttons()}",
        f"Axes: {joystick.get_numaxes()}",
        f"Hats: {joystick.get_numhats()}",
        f"Balls: {joystick.get_numballs()}",
    ]


def draw_text(surface, font, text, x, y, color=(255, 255, 255)):
    surface.blit(font.render(text, True, color), (x, y))
    return y + LINE_HEIGHT


def draw_joystick_state(surface, font, joystick, y):
    y = draw_text(surface, font, f"{joystick.get_name()}  (instance {joystick.get_instance_id()})", 8, y, (255, 255, 0))

    buttons_down = [str(i) for i in range(joystick.get_numbuttons()) if joystick.get_button(i)]
    y = draw_text(surface, font, f"Buttons down: {', '.join(buttons_down) if buttons_down else '-'}", 16, y)

    hats = [f"hat{h}={joystick.get_hat(h)}" for h in range(joystick.get_numhats())]
    y = draw_text(surface, font, f"Hats: {', '.join(hats) if hats else '-'}", 16, y)

    axes = [f"axis{a}={joystick.get_axis(a):+.2f}" for a in range(joystick.get_numaxes())]
    y = draw_text(surface, font, f"Axes: {', '.join(axes) if axes else '-'}", 16, y)

    return y + 10


def main():
    pygame.init()
    pygame.joystick.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Controller Diagnostic (temporary tool)")
    font = pygame.font.SysFont("consolas,couriernew,monospace", 16)
    clock = pygame.time.Clock()

    joysticks = {}

    def open_joystick(index):
        joystick = pygame.joystick.Joystick(index)
        joystick.init()
        instance_id = joystick.get_instance_id()
        is_new = instance_id not in joysticks
        joysticks[instance_id] = joystick
        if is_new:
            print(f"\n=== Controller connected (instance {instance_id}) ===")
            for line in describe_joystick(joystick):
                print(f"  {line}")

    for i in range(pygame.joystick.get_count()):
        open_joystick(i)

    if not joysticks:
        print("No joysticks detected yet. Plug in your controller - this tool")
        print("will pick it up automatically once Windows/pygame sees it.")

    print("\nPress every button and every D-pad direction now.")
    print("Each event is logged below as it happens. Close the window (or")
    print("Ctrl+C in the terminal) to quit.\n")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYDEVICEADDED:
                open_joystick(event.device_index)
            elif event.type == pygame.JOYDEVICEREMOVED:
                if joysticks.pop(event.instance_id, None) is not None:
                    print(f"Controller disconnected (instance {event.instance_id})")
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"[instance {event.instance_id}] BUTTON {event.button} DOWN")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"[instance {event.instance_id}] BUTTON {event.button} UP")
            elif event.type == pygame.JOYHATMOTION:
                print(f"[instance {event.instance_id}] HAT {event.hat} = {event.value}")
            elif event.type == pygame.JOYAXISMOTION:
                if abs(event.value) > AXIS_PRINT_DEADZONE:
                    print(f"[instance {event.instance_id}] AXIS {event.axis} = {event.value:+.3f}")

        screen.fill((20, 20, 24))
        y = 8
        if not joysticks:
            y = draw_text(screen, font, "No joystick detected.", 8, y)
        for joystick in joysticks.values():
            y = draw_joystick_state(screen, font, joystick, y)

        draw_text(screen, font, "Close this window (or Ctrl+C) to quit.", 8, WINDOW_SIZE[1] - 24, (150, 150, 150))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit(0)
