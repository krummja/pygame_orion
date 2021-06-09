from __future__ import annotations
from typing import TYPE_CHECKING

import ecstremity

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class ECSManager:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.engine = ecstremity.Engine(client = game)
        self.components = self.engine.components
        self.prefabs = self.engine.prefabs
