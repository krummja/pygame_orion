from __future__ import annotations
from typing import TYPE_CHECKING, List
import logging

import pygame as pg
from pygame_orion.core.emitter import EventEmitter
from pygame_orion._events import *

if TYPE_CHECKING:
    from pygame_orion.renderer.base_render_system import BaseRenderSystem
    from pygame_orion.core.game import Game
    from pygame_orion.scenes.scene import Scene

logger = logging.getLogger(__file__)


class Renderer:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.events = EventEmitter()

        self.game.events.on(BOOT, self._boot)
        self.game.events.on(READY, self._ready)

    def boot(self):
        pass

    def ready(self):
        pass

    def _boot(self):
        logger.info("BOOT: Renderer")
        self.boot()
        self.events.emit(BOOT, "Renderer")

    def _ready(self):
        logger.info("READY: Renderer")
        self.ready()
        self.events.emit(READY)

    def pre_render(self):
        self.game.display.surface.fill((0, 0, 64))

    def render(self, scene: Scene, time: float, delta: float) -> None:
        pass

    def post_render(self):
        pg.display.flip()
