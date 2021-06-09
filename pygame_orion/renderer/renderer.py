from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame_orion.core.game import Game
    from pygame_orion.scenes.scene import Scene


class Renderer:

    def __init__(self, game: Game) -> None:
        self.game = game

    def pre_render(self):
        pass

    def render(self):
        pass

    def render_scene(self, scene) -> None:
        pass

    def post_render(self):
        pass
