"""Entry point for the technical-prototype game. Run from the project
root: `python main.py`.

This is the composition root for the prototype specifically: it owns the
list of states this game has and which one starts first. engine.Game
itself has no opinion on that - see engine/game.py.
"""
from engine.game import Game
from games.prototype.states import BootState, TitleState, GameplayState, PauseState


def register_states(game):
    game.state_machine.register("BOOT", BootState(game))
    game.state_machine.register("TITLE", TitleState(game))
    game.state_machine.register("GAMEPLAY", GameplayState(game))
    game.state_machine.register("PAUSE", PauseState(game))
    game.state_machine.change("BOOT")


if __name__ == "__main__":
    Game(register_states).run()
