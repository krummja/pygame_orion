from __future__ import annotations
from typing import Any, Dict, Optional, Type
import logging

from pygame_orion.events import *
from pygame_orion.plugins import OrionPlugin, OrionPluginRegistry
from pygame_orion.core.config import OrionConfig
from pygame_orion.core.time_step import TimeStep


logger = logging.getLogger(__file__)


class BootManager:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.boot_status = {}
        self.game.events.on(READY, self.game.start)

        for key, plugin in OrionPluginRegistry.plugins().items():
            if key == "Game" or key == "OrionPlugin":
                continue
            self.boot_status[key] = False
            self.boot_plugin(plugin)

        for key in OrionPluginRegistry.plugins().keys():
            if key == "Game" or key == "OrionPlugin":
                continue
            plugin = OrionPluginRegistry.get_plugin(key)
            plugin.events.on(BOOT, self._set_ready)

    def boot_plugin(self, plugin: Type[OrionPlugin]) -> OrionPlugin:
        _plugin = plugin()
        OrionPluginRegistry.add_booted(_plugin)
        self.game.events.on(BOOT, _plugin._boot)
        self.game.events.on(READY, _plugin._ready)
        self.game.events.on(START, _plugin._start)
        return _plugin

    def _set_ready(self, key: str) -> None:
        self.boot_status[key] = True
        if all([value is True for value in self.boot_status.values()]):
            self.game.ready()


class Game(OrionPlugin):

    def __init__(
            self,
            options: Optional[Dict[str, Any]] = None,
            config_path: Optional[str] = None,
        ) -> None:
        """The core client object that serves as the central interface
        with the rest of the framework.

        Different packages that provide certain kinds of functionality
        can be dropped into this basic class like plugins.

        Access plugins using the `OrionPluginRegistry.plugins()` classmethod.
        Register them by extending the `OrionPlugin` class.

        Access plugins by key using the registry's `get_plugin` method, e.g.
            plugin = OrionPluginRegistry.get_plugin("MyPlugin")
        """
        self.config = OrionConfig(options, config_path)
        self.boot_manager = BootManager(self)
        self.loop = TimeStep(self)

        self._is_booted = False
        self._is_running = False
        self._pending_teardown = False
        self._remove_display = False

    def boot(self):
        logger.info("BOOT")
        self._is_booted = True
        self.events.emit(BOOT)

    def ready(self):
        logger.info("READY")
        self.events.emit(READY)

    def start(self):
        logger.info("All Orion Plugins report READY status. Starting main loop.")
        self.events.emit(START)

        self.events.on(STOP, self.stop)
        self._is_running = True
        self.loop.start(self.step)

    def step(self, time: float, delta: float):
        if self._pending_teardown:
            self.teardown()

        emitter = self.events

        emitter.emit(PRE_STEP, time, delta)
        emitter.emit(STEP, time, delta)
        emitter.emit(POST_STEP, time, delta)

        emitter.emit(PRE_RENDER, time, delta)
        emitter.emit(POST_RENDER, time, delta)

    def stop(self):
        self._is_running = False
        self._pending_teardown = True
        self.events.emit(TEARDOWN)

    def teardown(self):
        pass
