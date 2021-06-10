from __future__ import annotations
from typing import List, TYPE_CHECKING, Union, Optional, Dict, Any, Callable
from collections import deque
import logging

from pygame_orion.scenes import constants as CONST
from pygame_orion._events import *
from pygame_orion.core.emitter import EventEmitter

if TYPE_CHECKING:
    from pygame_orion.scenes.scene import Scene, SceneConfig, SceneSystems
    from pygame_orion.core.game import Game
    from pygame_orion.renderer.renderer import Renderer


logger = logging.getLogger(__file__)


class SceneHandler:

    def __init__(self, manager: SceneManager) -> None:
        self._manager = manager
        self._keys = {}
        self._scenes = []
        self.count = len(self._scenes)

    def push_scene(self, scene: Scene) -> None:
        self._scenes.append(scene)
        if scene.sys.settings.key not in self._keys.keys():
            self._keys[scene.sys.settings.key] = scene
        scene.manager = self._manager
        scene.manager.processor.add_to_pending(scene)

    def pop_scene(self, idx: Optional[int] = None, delete_key: bool = True) -> Scene:
        if idx is not None:
            scene = self._scenes.pop(idx)
        else:
            scene = self._scenes.pop()
        if delete_key:
            del self._keys[scene.sys.settings.key]
        return scene

    def remove_scene(self, key_or_scene: Union[str, Scene]) -> None:
        if isinstance(key_or_scene, str):
            scene = self._keys.get(key_or_scene)
            if scene:
                self._scenes.remove(scene)
                del self._keys[scene.sys.settings.key]
        elif isinstance(key_or_scene, Scene):
            self._scenes.remove(key_or_scene)
            del self._keys[key_or_scene.sys.settings.key]
        else:
            raise TypeError(f"Expected scene key or scene instance. Got {type(key_or_scene)}.")

    def set_scene_to_top(self, key_or_scene: Union[str, Scene]) -> None:
        if isinstance(key_or_scene, str):
            pass
        elif isinstance(key_or_scene, Scene):
            scene = self.pop_scene(False)
            self.push_scene(scene)
        else:
            raise TypeError(f"Expected scene key or scene instance. Got {type(key_or_scene)}.")


class SceneProcessor:

    def __init__(self, manager: SceneManager) -> None:
        self._manager = manager
        self._pending = deque([])
        self._start = deque([])
        self._queue = deque([])
        self._is_processing: bool = False

    def add_to_pending(self, scene: Scene) -> None:
        self._pending.append(scene)

    def process_pending(self):
        if not self._pending:
            return
        scene = self._pending.popleft()
        sys = scene.sys
        sys.settings.status = CONST.INIT

        if hasattr(scene, "start"):
            self.start(scene)
        if hasattr(scene, "preload"):
            self.preload(scene)
        if hasattr(scene, "create"):
            self.create(scene)

        sys.settings.status = CONST.RUNNING
        self._add_to_queue(scene)

    # Scene Lifecycle API

    def start(self, scene: Scene) -> None:
        """Set up the scene and prepare for preloading."""
        scene.sys.settings.status = CONST.START
        logger.info(f"START: {scene.sys.settings.key}")
        scene.start()

    def preload(self, scene: Scene) -> None:
        """Load up any necessary resources for game object creation."""
        scene.sys.settings.status = CONST.LOADING
        logger.info(f"PRELOAD: {scene.sys.settings.key}")
        scene.preload()

    def create(self, scene: Scene) -> None:
        """Instantiate instances of game objects."""
        scene.sys.settings.status = CONST.CREATING
        logger.info(f"CREATE: {scene.sys.settings.key}")
        scene.create()

    def update(self, time: float, delta: float) -> None:
        self._is_processing = True
        self.process_pending()
        for scene in self._queue:
            scene.update(time, delta)

    def render(self, renderer: Renderer) -> None:
        for scene in self._queue:
            sys: SceneSystems = scene.sys
            if (sys.settings.visible
                    and sys.settings.status >= CONST.LOADING
                    and sys.settings.status <= CONST.SLEEPING):
                sys.render(renderer)
        self._is_processing = False

    # Internal API

    def _add_to_queue(self, scene: Scene) -> None:
        self._queue.append(scene)


class SceneManager:

    def __init__(self, game: Game) -> None:
        self.game = game
        self.events = EventEmitter()

        self.is_booted: bool = False
        self.handler = SceneHandler(self)
        self.processor = SceneProcessor(self)
        self.count = self.handler.count

        self.game.events.on(BOOT, self._boot)
        self.game.events.on(READY, self._ready)

    def boot(self):
        """Can be overridden to provide on-boot functionality."""
        pass

    def ready(self):
        """Can be overridden to provide on-ready functionality."""
        pass

    def _boot(self):
        logger.info("BOOT: SceneManager")
        self.boot()
        self.events.emit(BOOT, "Scene")

    def _ready(self):
        logger.info("READY: SceneManager")
        self.ready()
        self.events.emit(READY)

    # Handler API

    def add(self, scene: Scene) -> None:
        logger.info(f"Adding scene: {scene.sys.settings.key}")
        self.handler.push_scene(scene)

    def remove(self, scene: Scene) -> None:
        logger.info(f"Removing scene: {scene.sys.settings.key}")
        self.handler.remove_scene(scene)

    def remove_by_key(self, key: str) -> None:
        logger.info(f"Removing scene with key {key}")
        self.handler.remove_scene(key)

    # Processor API

    def update(self, time: float, delta: float):
        self.processor.update(time, delta)

    def render(self, renderer: Renderer) -> None:
        self.processor.render(renderer)
