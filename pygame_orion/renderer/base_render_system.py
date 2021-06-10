from __future__ import annotations
from typing import TYPE_CHECKING, List

import pygame as pg
from pygame_orion.ecs.base_system import BaseSystem

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class BaseRenderSystem(BaseSystem):

    def __init__(self, game: Game) -> None:
        super().__init__(game)

    def initialize(self) -> None:
        pass

    def update(self, time: float, delta: float) -> List[pg.Surface]:
        pass
