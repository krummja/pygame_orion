from __future__ import annotations
from typing import TYPE_CHECKING
import logging

from pygame_orion.core.emitter import EventEmitter
from pygame_orion._events import *

import ecstremity

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


logger = logging.getLogger(__file__)


class ECSManager:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.events = EventEmitter()
        self.engine = ecstremity.Engine(client = game)
        self.components = self.engine.components
        self.prefabs = self.engine.prefabs

        self.game.events.on(BOOT, self._boot)
        self.game.events.on(READY, self._ready)

    def boot(self):
        pass

    def ready(self):
        pass

    def _boot(self):
        logger.info("BOOT: ECSManager")
        self.boot()
        self.events.emit(BOOT, "ECS")

    def _ready(self):
        logger.info("READY: ECSManager")
        self.ready()
        self.events.emit(READY)
