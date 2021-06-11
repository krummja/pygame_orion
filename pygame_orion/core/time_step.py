from __future__ import annotations
from typing import TYPE_CHECKING

import pygame as pg
import pygame_orion._logging as log

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class TimeStep:

    def __init__(self, game: Game) -> None:
        log.configure(game.config)
        self.game = game

        self.clock = pg.time.Clock()
        self.runtime = 0
        self.frame = 0
        self.ticks = 0

        self._callback = None
        self._started = False
        self._is_running = False
        self._start_time = 0
        self._last_time = 0
        self._now = 0

    def start(self, callback) -> None:
        if self._started:
            return

        self._callback = callback
        self._started = True
        self._is_running = True
        self._start_time = self.clock.get_time()

        while self._is_running:
            self.step()

    def step(self):
        self._now = time = self.clock.get_time()
        dt = time - self._last_time

        self.runtime += dt
        self._callback(time, dt)
        self.clock.tick()

        self._last_time = time
        self.ticks += 1
        self.frame += 1

    def stop(self):
        self._is_running = False
        self._started = False
        self.teardown()

    def teardown(self):
        self._callback = None
        self.game = None

    def tick(self):
        self.tick()
