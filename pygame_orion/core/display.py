from __future__ import annotations
from typing import TYPE_CHECKING, Union, List, Tuple

import pygame

if TYPE_CHECKING:
    from pygame import Vector2
    from pygame_orion.core.game import Game


class Display:

    def __init__(self, game: Game) -> None:
        self.game = game
        self._surface = pygame.display.get_surface()

    @property
    def surface(self):
        return self._surface
