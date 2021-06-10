import unittest as test
import pygame_orion as orion
from pygame_orion.scenes.scene import Scene


class TestScene(Scene):

    def __init__(self):
        super().__init__({
            "key": "test_scene"
        })

    def preload(self):
        print("Scene has preload method!")

    def update(self, time: float, delta: float):
        print("Updating!")


class TestOrion(test.TestCase):

    def setUp(self) -> None:
        self.orion = orion.Game()

    def testScenes(self) -> None:
        self.orion.scene.add(TestScene())
        self.orion.boot()


if __name__ == '__main__':
    test.main()
