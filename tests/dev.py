from __future__ import annotations
from typing import Tuple, List
import pygame as pg
import pygame_orion as orion


class InputHandler(orion.InputHandler):

    def cmd_confirm(self):
        print("Hello!")

    def cmd_escape(self):
        self.scene.sys.game_events.emit(orion.EVENTS.STOP)

    def cmd_test(self):
        print("Test!")


class TestScene(orion.Scene):

    def __init__(self):
        super().__init__({
            "key": "test_scene",
            "visible": True,
            "active": True,
            "input": {
                "handler": InputHandler(self),
                "command_keys": {
                    pg.K_SPACE: "test"
                }
            }
        })

    def update(self, time: float, dt: float) -> None:
        pass


class Game(orion.Game):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    game = Game()
    game.scene.add(TestScene())
    game.boot()
