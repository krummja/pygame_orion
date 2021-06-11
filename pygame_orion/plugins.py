from __future__ import annotations
from typing import Dict, Optional

from pygame_orion.events import *

from pygame_orion.core.events import EventEmitter


class OrionPluginRegistry(type):
    REGISTRY = {}
    BOOTED = {}

    def __new__(mcs, name, bases, attrs):
        clsobj = type.__new__(mcs, name, bases, attrs)
        mcs.REGISTRY[clsobj.__name__] = clsobj
        clsobj.events = EventEmitter()
        return clsobj

    @classmethod
    def plugins(mcs):
        return dict(mcs.REGISTRY)

    @classmethod
    def add_booted(mcs, plugin):
        mcs.BOOTED[plugin.__class__.__name__] = plugin

    @classmethod
    def get_plugin(mcs, key: str) -> OrionPlugin:
        if key in mcs.BOOTED.keys():
            return mcs.BOOTED[key]
        return mcs.REGISTRY[key]


class OrionPlugin(metaclass=OrionPluginRegistry):
    """Base class for registering plugins to the Orion framework.

    All OrionPlugins come equipped with an EventEmitter to handle
    inter-plugin communications.
    """

    def _boot(self):
        self.events.emit(BOOT, str(self.__class__.__name__))
        self.boot()

    def _ready(self):
        self.events.emit(READY, str(self.__class__.__name__))
        self.ready()

    def _start(self):
        self.events.emit(START, str(self.__class__.__name__))
        self.start()

    def boot(self):
        raise NotImplementedError

    def ready(self):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError
