from __future__ import annotations
from typing import List, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from pygame_orion.scenes.scene import Scene
    from pygame_orion.core.game import Game


class SceneManager:

    def __init__(self, game: Game) -> None:
        self._game = game
        self._keys = {}
        self._scenes = []
        self._pending = []
        self._start = []
        self._queue = deque([])
        self._is_processing: bool = False
        self._is_booted: bool = False

    @property
    def game(self) -> Game:
        return self._game

    def push_scene(self, scene: Scene) -> None:
        pass

    def update(self, time: float, delta: float):
        pass

    def render(self, renderer):
        pass
