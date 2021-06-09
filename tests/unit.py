import unittest as test
import pygame_orion as orion


class TestOrion(test.TestCase):

    def setUp(self) -> None:
        self.orion = orion.Game()

    def testStart(self) -> None:
        self.orion.boot()


if __name__ == '__main__':
    test.main()
