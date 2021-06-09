from __future__ import annotations
from typing import TYPE_CHECKING, Union, Dict, Any
from collections import OrderedDict

from pygame_orion.core.events import EventEmitter
from pygame_orion.scenes import events
from pygame_orion.scenes import constants

if TYPE_CHECKING:
    from pygame_orion.renderer.renderer import Renderer
    from pygame_orion.scenes.scene_manager import SceneManager
    from pygame_orion.core.game import Game


class SceneSettings:

    def __init__(self, scene: Scene, config: Dict[str, Any]) -> None:
        self.scene = scene
        self.key = config["key"]
        self.status: int = constants.INIT
        self.visible: bool = config.get("visible", True)


class SceneSystems:

    def __init__(self, scene: Scene, settings: SceneSettings) -> None:
        self.scene = scene
        self.settings = settings
        self.events = EventEmitter()

    def render(self, renderer: Renderer) -> None:
        renderer.render_scene(self.scene)


class Scene:

    def __init__(self, config: Dict[str, Any] = None) -> None:
        """A base Scene object that can be extended for your own use.

        You may optionally override the lifecycle methods `start()`,
        `preload()`, and `create()`.

        SceneManager Boot:
            - manager.events.on('BOOT', self.boot)

        Every tick:
            - manager.events.on('PRE_UPDATE', self.pre_update)
            - manager.events.on('UPDATE', self.update, time, dt)
            - manager.events.on('POST_UPDATE', self.post_update)
            - manager.events.on('RENDER', self.render)

        State changed:
            - manager.events.on('PAUSE', self.pause)
            - manager.events.on('RESUME', self.resume)
            - manager.events.on('SLEEP', self.sleep)
            - manager.events.on('WAKE', self.wake)
            - manager.events.on('STOP', self.stop)

        Teardown:
            - manager.events.on('TEARDOWN', self.teardown)

        Game objects:
            - manager.events.on('ADDED_TO_SCENE', self.added, obj, scene)
            - manager.events.on('REMOVED_FROM_SCENE', self.removed, obj, scene)
        """
        settings = SceneSettings(self, config or {"key": "scene_" + str(self._manager.count)})
        self._systems = SceneSystems(self, settings)
        self._manager: Union[SceneManager, None] = None

    @property
    def sys(self):
        return self._systems

    def update(self, time: float, delta: float):
        raise NotImplementedError

    @property
    def manager(self) -> SceneManager:
        return self._manager

    @manager.setter
    def manager(self, value: SceneManager) -> None:
        self._manager = value

    # Event Hooks

    def _pre_update(self) -> None:
        pass

    def _post_update(self) -> None:
        pass

    def _render(self) -> None:
        pass

    # State Management API

    def _pause(self) -> None:
        pass

    def _resume(self) -> None:
        pass

    def _sleep(self) -> None:
        pass

    def _wake(self) -> None:
        pass

    def _stop(self) -> None:
        pass
