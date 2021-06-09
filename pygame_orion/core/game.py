from __future__ import annotations
import logging

from pygame.time import Clock

import pygame_orion.core.events as events
import pygame_orion._logging as log

from pygame_orion.core.config import OrionConfig
from pygame_orion.core.display import Display
from pygame_orion.core.events import EventEmitter
from pygame_orion.renderer.renderer import Renderer
from pygame_orion.scenes.scene_manager import SceneManager
from pygame_orion.ecs.ecs_manager import ECSManager
from pygame_orion.input.input_manager import InputManager
from pygame_orion._prepare import CONFIG


class MainLoop:

    def __init__(self, game: Game) -> None:
        log.configure()

        self.game = game
        self.clock = Clock()
        self.callback = None
        self.runtime = 0
        self.frame = 0
        self.ticks = 0

        self._started = False
        self._is_running = False
        self._start_time = 0
        self._last_time = 0
        self._now = 0

    def run(self, stop):
        while self._is_running:
            self.step()

            if self.ticks >= stop:
                self.stop()

    def start(self, callback):
        if self._started:
            return
        self.callback = callback
        self._started = True
        self._is_running = True
        self._start_time = self.clock.get_time()
        self.run(10)

    def step(self):
        time = self.clock.get_time()
        self._now = time
        before = time - self._last_time
        dt = before
        self.runtime += dt
        self.callback(time, dt)
        self.clock.tick()
        self._last_time = time
        self.ticks += 1
        self.frame += 1

    def stop(self):
        self._is_running = False
        self._started = False
        return self

    def teardown(self):
        self.stop()
        self.callback = None
        self.game = None

    def tick(self):
        self.step()


class Game:

    def __init__(self) -> None:
        self.config: OrionConfig = CONFIG

        self.events = EventEmitter()
        self.renderer: Renderer = Renderer(self)
        self.display: Display = Display(self)

        self.input: InputManager = InputManager(self)
        self.ecs: ECSManager = ECSManager(self)
        self.scene: SceneManager = SceneManager(self)

        self.loop: MainLoop = MainLoop(self)

        self._is_booted = False
        self._is_running = False
        self._pending_teardown = False
        self._remove_display = False

    def boot(self) -> None:
        self._is_booted = True
        self.events.emit(events.BOOT)
        self.ready()

    def ready(self) -> None:
        self.events.emit(events.READY)
        self.start()

    def start(self) -> None:
        self._is_running = True
        if self.renderer:
            self.loop.start(self.step)

    def step(self, time: float, delta: float) -> None:
        if self._pending_teardown:
            return self.teardown()

        emitter = self.events

        # Global Managers like Input and Sound update here
        emitter.emit(events.PRE_STEP, time, delta)

        # User code and plugins
        emitter.emit(events.STEP, time, delta)

        # Update the SceneManager and all active Scenes
        self.scene.update(time, delta)

        # Final event before rendering starts
        emitter.emit(events.POST_STEP)

        renderer = self.renderer

        # Run the Pre-Render (clear the display, set background colors, etc.)
        renderer.pre_render()
        emitter.emit(events.PRE_RENDER, renderer, time, delta)

        # The main render loop. Iterates all Scenes and all Cameras in those scenes, rendering to the render instance.
        self.scene.render(renderer)

        # Post-Render call. Tidies up loose ends, takes snapshots, etc.
        renderer.post_render()

        # The final event before the step repeats. Last chance to do anything to the display.
        emitter.emit(events.POST_RENDER, renderer, time, delta)

    def teardown(self) -> None:
        pass
