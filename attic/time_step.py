from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional, Union
import time as _time

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class MainLoop:

    def __init__(self):
        self._is_running = False
        self.callback = None
        self.tick = 0
        self.last_time = 0
        self.target = 0

    def step(self):
        timestamp = time.time()
        self.last_time = self.tick
        self.tick = timestamp
        self.callback(timestamp)

    def start(self, callback, target_fps: float):
        if self._is_running:
            return

        self.callback = callback
        self.target = target_fps
        self._is_running = True

    def stop(self):
        pass

    def teardown(self):
        pass


class TimeStep:

    def __init__(self, game: Game, fps: int) -> None:
        self.game = game
        self.fps = fps

        self.loop = MainLoop()

        self._started = False
        self._running = False

        self._min_fps = game.config.min_fps or 5
        self._target_fps = game.config.fps or 60
        self._smooth_step = game.config.smooth_step or True
        self._min = 1000 / self._min_fps
        self._target = 1000 / self._target_fps
        self.actual_fps = self._target_fps
        self.next_fps_update = 0
        self.frames_this_second = 0

        self.time = 0
        self.start_time = 0
        self.frame = 0

        self.in_focus = True
        self._pause_time = 0
        self._cool_down = 0

        self.raw_delta = 0
        self.delta = 0
        self.delta_index = 0
        self.delta_history = []
        self.delta_smoothing_max = game.config.delta_history or 10

        self.now = 0
        self.last_time = 0
        self.callback: Union[Callable[[float, float, Optional[float]], None], None] = None

    def pause(self):
        pass

    def resume(self):
        pass

    def reset_delta(self):
        pass

    def start(self, callback) -> Optional[TimeStep]:
        """Start the TimeStep.

        `callback` is the `step` method of our `Game` object.
        """
        if self._started:
            return self

        self._started = True
        self._running = True

        for i in range(self.delta_smoothing_max):
            self.delta_history[i] = self._target

        self.reset_delta()
        self.start_time = time.time()
        self.callback = callback
        self.loop.start(self.step, self._target)

    def step(self):
        time = _time.time()
        self.now = time
        before = time - self.last_time
        self.raw_delta = before

        avg = before

        self.delta = avg
        self.time += self.raw_delta

        if time > self.next_fps_update:
            self.actual_fps = 0.25 * self.frames_this_second + 0.75 * self.actual_fps
            self.next_fps_update = time + 1000
            self.frames_this_second = 0

        self.frames_this_second += 1

        interpolation = avg / self._target

        self.callback(time, avg, interpolation)
        self.last_time = time
        self.frame += 1

    def tick(self):
        self.step()

    def sleep(self):
        if self._running:
            self.loop.stop()
            self._running = False

    def wake(self):
        if self._running:
            return
        self.loop.start(self.step, self._target)
        self._running = True
        self.step()

    def get_duration(self):
        pass

    def get_duration_ms(self):
        pass

    def stop(self):
        pass

    def teardown(self):
        pass
