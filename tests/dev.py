from __future__ import annotations
from typing import Tuple, List
import pygame as pg
import pygame_orion as orion


class Game(orion.Game):

    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    game = Game()
    game.boot()
