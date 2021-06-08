from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class TimeStep:

    def __init__(self, game: Game, fps: int) -> None:
        self.game = game
        self.fps = fps

        self._started = False
        self._running = False

        self._min_fps = getattr(game.config, 'min') or 5
        self._target_fps = getattr(game.config, 'target') or 60
        self._min = 1000 / self._min_fps
        self._target = 1000 / self._target_fps
        self.actual_fps = self._target_fps

        self.time = 0
        self.start_time = 0
        self.frame = 0

        self.in_focus = True
        self._pause_time = 0
        self._cool_down = 0
        self.delta = 0
        self.delta_index = 0
        self.delta_history = []

        self.now = 0

    def pause(self):
        pass

    def resume(self):
        pass

    def reset_delta(self):
        pass

    def start(self, callback):
        pass

    def step(self):
        pass

    def tick(self):
        pass

    def sleep(self):
        pass

    def wake(self):
        pass

    def get_duration(self):
        pass

    def get_duration_ms(self):
        pass

    def stop(self):
        pass

    def teardown(self):
        pass
