"""Entry point for Alphabet Excavation. Run as a module from the project
root (NOT as a direct file path - see note below):
    python -m games.alphabet_excavation.main

Must be run with -m: running this file directly (`python
games/alphabet_excavation/main.py`) puts this file's own folder on
sys.path[0] instead of the project root, and `import engine` fails.
`-m` resolves imports against the current working directory instead, so
it must be run from the project root.

This is the composition root for this game specifically: it owns the
list of states this game has and which one starts first. engine.Game
itself has no opinion on that - see engine/game.py.
"""
from engine.game import Game
from games.alphabet_excavation.states import Level1State

SETTINGS_PATH = "games/alphabet_excavation/data/settings.json"


def register_states(game):
    game.state_machine.register("LEVEL_1", Level1State(game))
    game.state_machine.change("LEVEL_1")


if __name__ == "__main__":
    Game(register_states, settings_path=SETTINGS_PATH).run()
