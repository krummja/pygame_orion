from __future__ import annotations
from typing import Dict, List, Optional, Any, Tuple

import pygame_orion.core.events as events

from pygame_orion.core.config import OrionConfig
from pygame_orion.core.display import Display
from pygame_orion.core.events import EventEmitter
from pygame_orion.core.time_step import TimeStep
from pygame_orion.renderer.renderer import Renderer
from pygame_orion.scenes.scene_manager import SceneManager


class Config:

    def __init__(self, config: Dict[str, Any]):
        self.fps: int = config["fps"]
        self.command_keys: Dict[int, str] = config["command_keys"]
        self.move_keys: Dict[int, Tuple[int, int]] = config["move_keys"]


class Game:

    def __init__(self, config_path: str) -> None:
        self.config: OrionConfig = OrionConfig(config_path)
        self.renderer: Renderer = Renderer(self)
        self.display: Display = Display(self)

        self._is_booted = False
        self._is_running = False

        self.events = EventEmitter(self)
        self.cache = None  # TODO CacheManager(self)
        self.registry = None  # TODO DataManager(self)
        self.input = None  # TODO InputManager(self, self.config)
        self.scene = SceneManager(self)
        self.loop = TimeStep(self, self.config.fps)

        self._pending_teardown = False
        self._remove_display = False

        self.boot()

    def boot(self):
        pass

    def preload(self):
        # emit Events.READY
        self.start()

    def start(self):
        pass

    def step(self, time: float, delta: float):
        if self._pending_teardown:
            return self.teardown()

        emitter = self.events

        # Global Managers like Input and Sound update here
        emitter.emit(events.PRE_STEP, time, delta)

        # User code and plugins
        emitter.emit(events.STEP, time, delta)

        # Update the SceneManager and all active Scenes
        this.scene.update(time, delta)

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

    def get_frame(self):
        pass

    def get_time(self):
        pass

    def teardown(self):
        pass

