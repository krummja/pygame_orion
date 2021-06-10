Introduction
============

Orion is an opinionated game development framework built on top of Pygame. It started as a small project aiming to make a grab-bag of utilities for my own Pygame projects, but as I worked out details and the project grew, I decided to flesh it out into a fully-fledged framework. Besides Pygame, Orion also uses `Pygame GUI <https://www.github.com/MyreMylar/pygame_gui>`_ for interface development and my own ECS engine `ECStremity <https://www.github.com/krummja/ecstremity>`_ for... well, ECS stuff.

Features
--------

- All of the features of Pygame 2.
- A `Phaser 3 <https://phaser.io>`_ flavored game loop, chock-full of lifecycle events for hooking in your own modules and plugins in sync with the engine's heartbeat.
- Quick GUI construction using Pygame GUI, with some of my own interfaces to the package.
- A full-featured ECS engine to make quick work of development and complex game object interaction.
- An input handling module that abstracts some of the I/O functionality of Pygame into an easier to use interface.
- A rendering module that comes with helpful utilities for working with Pygame surfaces.


Installation
------------
Install the latest release from PyPi using pip with:

.. code-block:: console

    pip install pygame_orion -U

You can also build the latest version `from Github here <https://www.github.com/krummja/pygame_orion>`_ by downloading the source, navigating to the project's directory (which contains ``setup.py``) and building with:

.. code-block:: console

    python setup.py install
    pip install . -U

Source Code on Github
---------------------

The source code is `available from Github here <https://www.github.com/krummja/pygame_orion>`_.

Quick Start Guide
-----------------

Using Orion assumes some basic familiarity with Pygame. Additionally, it will be useful to be acquainted with Pygame GUI and, at the very least, what an ECS is. There are many helpful tutorials and guides across the internet, but I recommend checking out the following as a baseline:

- `Pygame <https://www.pygame.org/docs/>`_
- `Pygame GUI <https://pygame-gui.readthedocs.io/en/latest/index.html>`_
- ECStremity (under construction)

To begin a project using Orion, simply import the library and start with a basic scene object:

.. code-block:: python
   :linenos:

   import pygame_orion as orion


   class InputHandler(orion.InputHandler):

      def cmd_escape(self):
         self.scene.sys.game_events.emit(orion.EVENTS.STOP)


   class StartScene(orion.Scene):

      def __init__(self) -> None:
         super().__init__({
            "key": "start",
            "visible": True,
            "active": True,
            "input": {
               "handler": InputHandler(self)
            },
         })

      def update(self, time: float, dt: float) -> None:
         pass


   class Game(orion.Game):

      def __init__(self):
         super().__init__()


   if __name__ == '__main__':
      game = Game()
      game.scene.add(StartScene())
      game.boot()

When you execute the above, nothing of particular interest will happen. A black screen will appear, which can be closed by pressing ``ESC`` on your keyboard. Let's break down what's going on. To begin with, we extended an ``InputHandler`` object,


Examples
--------

