from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, Any
from collections import OrderedDict

from pygame_orion._events import *
from pygame_orion.core.emitter import EventEmitter
from pygame_orion.scenes import constants as CONST
from pygame_orion.input.input_manager import InputHandler

if TYPE_CHECKING:
    from pygame_orion.renderer.renderer import Renderer
    from pygame_orion.scenes.scene_manager import SceneManager
    from pygame_orion.core.game import Game


class SceneConfig:

    def __init__(self, scene: Scene, config: Dict[str, Any]) -> None:
        self.scene = scene
        self.status: int = CONST.PENDING

        self.key: str = config.get("key")
        self.active: bool = config.get("active", True)
        self.visible: bool = config.get("visible", True)
        self.renderer = config.get("renderer")  # TODO pass in a default renderer?
        self.cameras = config.get("cameras")
        self.map = config.get("map", {})
        self.physics = config.get("physics", {})
        self.loader = config.get("loader", {})
        self.plugins = config.get("plugins", False)
        self.input = config.get("input", {
            "handler": InputHandler(self.scene),
            "command_keys": {},
            "move_keys": {},
        })


class SceneSystems:

    def __init__(self, scene: Scene, settings: SceneConfig) -> None:
        self.scene = scene
        self.settings = settings
        self.events = EventEmitter()
        self.input = self.settings.input["handler"]
        self.renderer = self.settings.renderer

    @property
    def game(self):
        return self.scene.manager.game

    @property
    def game_events(self):
        return self.game.events

    def render(self, renderer: Renderer, time: float, delta: float) -> None:
        renderer.render(self.scene, time, delta)


class Scene:

    def __init__(self, config: Dict[str, Any] = None) -> None:
        """A base Scene object that can be extended for your own use.

        You may optionally add the lifecycle methods `start()`,
        `preload()`, and `create()`.
        """
        settings = SceneConfig(self, config or {"key": "scene_" + str(self._manager.count)})
        self._systems = SceneSystems(self, settings)
        self._manager: Union[SceneManager, None] = None

    @property
    def sys(self):
        return self._systems

    @property
    def manager(self) -> SceneManager:
        return self._manager

    @manager.setter
    def manager(self, value: SceneManager) -> None:
        self._manager = value

    def update(self, time: float, delta: float):
        raise NotImplementedError
