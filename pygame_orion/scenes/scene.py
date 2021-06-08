from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame_orion.scenes.scene_manager import SceneManager
    from pygame_orion.core.game import Game


class Scene:

    def __init__(self, manager: SceneManager) -> None:
        self._manager = manager
        self._game = manager.game

    @property
    def manager(self) -> SceneManager:
        """The SceneManager that this Scene belongs to."""
        return self._manager

    @property
    def game(self) -> Game:
        """The Game that this Scene belongs to."""
        return self._game
