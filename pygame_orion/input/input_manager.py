from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Optional, Tuple, Dict, Generic
import logging

from pygame.locals import *
import pygame as pg

from pygame_orion._constants import *
from pygame_orion._events import *
from pygame_orion.core.emitter import EventEmitter

if TYPE_CHECKING:
    from pygame_orion.scenes.scene import Scene
    from pygame_orion.core.game import Game

logger = logging.getLogger(__file__)


T = TypeVar("T")


def get() -> Iterator[Any]:
    """A simple alias for pygame.event.get()."""
    return pg.event.get()


class InputDispatch(Generic[T]):

    def dispatch(self, event: Any) -> Optional[T]:
        event_type = pg.event.event_name(event.type)
        if event_type is None:
            return None
        if event_type in [
            "KeyDown",
            "Quit",
            "MouseMotion",
            "MouseButtonDown",
            "MouseButtonUp",
            "UserEvent"
        ]:
            func = getattr(self, "ev_%s" % (event_type.lower(),))
            return func(event)

    def ev_quit(self, event: pg.QUIT) -> Optional[T]:
        """Called when the termination of the program is requested."""

    def ev_keydown(self, event: KEYDOWN) -> Optional[T]:
        pass

    def ev_keyup(self, event: KEYUP) -> Optional[T]:
        pass

    def ev_mousemotion(self, event) -> Optional[T]:
        pass

    def ev_mousebuttondown(self, event) -> Optional[T]:
        pass

    def ev_mousebuttonup(self, event) -> Optional[T]:
        pass

    def ev_mousewheel(self, event) -> Optional[T]:
        pass

    def ev_userevent(self, event) -> Optional[T]:
        pass

    def ev_(self, event: Any) -> Optional[T]:
        pass


class PointerData:
    cursor: Optional[pg.Rect] = None
    scale: int = 3
    x: int = 0
    y: int = 0
    click: bool = False


class InputManager(Generic[T], InputDispatch[T]):

    _command_keys: Dict[int, str] = {
        K_RETURN: "confirm",
        K_ESCAPE: "escape"
    }
    _move_keys: Dict[int, Tuple[int, int]] = {}

    def __init__(self, game: Game) -> None:
        self.game = game
        self.display = None

        self.pointer_data = PointerData()

        self.events = EventEmitter()

        self.game.events.on(BOOT, self._boot)
        self.game.events.on(READY, self._ready)
        self.game.events.on(PRE_STEP, self.handle_input)

    def boot(self):
        pass

    def ready(self):
        pass

    def _boot(self):
        logger.info("BOOT: InputManager")
        self.display = self.game.display

        self.boot()
        self.events.emit(BOOT, "Input")

    def _ready(self):
        logger.info("READY: InputManager")

        input_scene = self.game.scene.handler.active_scene
        self._command_keys.update(input_scene.sys.settings.input.get("command_keys", {}))
        self._move_keys.update(input_scene.sys.settings.input.get("move_keys", {}))

        self.ready()
        self.events.emit(READY)

    def handle_input(self, _time: float, _delta: float) -> Optional[T]:
        for event in pg.event.get():
            value: T = self.dispatch(event)
            if value is not None:
                return value

    def ev_quit(self, event: QUIT) -> Optional[T]:
        return self.cmd_escape()

    def ev_keydown(self, event: KEYDOWN) -> Optional[T]:
        func: Callable[[], Optional[T]]
        key = event.__dict__['key']
        handler = self.game.scene.input

        if key in self._command_keys:
            func = getattr(handler, f"cmd_{self._command_keys[key]}")
            return func()
        elif key in self._move_keys:
            return handler.cmd_move(*self._move_keys[key])
        return None

    def ev_mousemotion(self, event: MOUSEMOTION) -> Optional[T]:
        self.pointer_data.x = event.pos[0]
        self.pointer_data.y = event.pos[1]
        return None

    def ev_mousebuttondown(self, event: MOUSEBUTTONDOWN) -> Optional[T]:
        if event:
            self.pointer_data.click = True
        return False

    def ev_mousebuttonup(self, event: MOUSEBUTTONUP) -> Optional[T]:
        if event:
            self.pointer_data.click = False
        return False


class InputHandler:

    def __init__(self, scene: Scene) -> None:
        self.scene = scene

    def cmd_move(self, x: int, y: int) -> None:
        pass

    def cmd_confirm(self) -> None:
        pass

    def cmd_escape(self) -> None:
        pass
