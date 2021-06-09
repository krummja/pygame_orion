from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class Renderer:

    def __init__(self, game: Game) -> None:
        self.game = game

    def pre_render(self):
        print("pre_render")

    def render(self):
        print("render")

    def post_render(self):
        print("post_render")
