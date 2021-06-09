from __future__ import annotations
from typing import TYPE_CHECKING, TypeVar, Optional, Tuple, Dict, Generic
import pygame as pg

from pygame_orion._constants import *

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


T = TypeVar("T")


def get() -> Iterator[Any]:
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

    def __init__(
            self,
            game: Game,
            command_keys: Optional[Dict[int, str]] = None,
            move_keys: Optional[Dict[int, Tuple[int, int]]] = None
        ) -> None:
        self.game = game
        self.pointer_data = PointerData()
        self.display = None
        self.command_keys = command_keys or {}
        self.move_keys = move_keys or {}

    def boot(self):
        self.display = self.game.display
        self._command_keys.update(self.command_keys)
        self._move_keys.update(self.move_keys)

    def update(self, _time: float, _delta: float) -> Optional[T]:
        for event in pg.event.get():
            try:
                value: T = self.dispatch(event)
            except StateBreak:
                return None
            if value is not None:
                return value

    def ev_quit(self, event: QUIT) -> Optional[T]:
        return self.cmd_escape()

    def ev_keydown(self, event: KEYDOWN) -> Optional[T]:
        func: Callable[[], Optional[T]]
        key = event.__dict__['key']
        if key in self._command_keys:
            func = getattr(self, f"cmd_{self._command_keys[key]}")
            return func()
        elif key in self._move_keys:
            return self.cmd_move(*self._move_keys[key])
        return None

    def ev_mousemotion(self, event: MOUSEMOTION) -> Optional[T]:
        self.client.ui.pointer_data.x = event.pos[0]
        self.client.ui.pointer_data.y = event.pos[1]
        return None

    def ev_mousebuttondown(self, event: MOUSEBUTTONDOWN) -> Optional[T]:
        if event:
            self.client.ui.pointer_data.click = True
        return False

    def ev_mousebuttonup(self, event: MOUSEBUTTONUP) -> Optional[T]:
        if event:
            self.client.ui.pointer_data.click = False
        return False
