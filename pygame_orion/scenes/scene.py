from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, Any
from collections import OrderedDict

from pygame_orion._events import *
from pygame_orion.core.emitter import EventEmitter
from pygame_orion.scenes import constants as CONST

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
        self.cameras = config.get("cameras")
        self.map = config.get("map", {})
        self.physics = config.get("physics", {})
        self.loader = config.get("loader", {})
        self.plugins = config.get("plugins", False)
        self.input = config.get("input", {})


class SceneSystems:

    def __init__(self, scene: Scene, settings: SceneConfig) -> None:
        self.scene = scene
        self.settings = settings
        self.events = EventEmitter()

    def render(self, renderer: Renderer) -> None:
        renderer.render_scene(self.scene)


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
