"""A straightforward event emitter,
based on https://github.com/etissieres/PyEventEmitter
"""
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pygame_orion.core.game import Game


class ListenerWrapper:

    def __init__(self, listener, is_once=False):
        self.listener = listener
        self.is_once = is_once

    def __call__(self, *args, **kwargs):
        self.listener(*args, **kwargs)

    def __eq__(self, other):
        if isinstance(other, ListenerWrapper):
            return other.listener == self.listener
        if isinstance(other, types.FunctionType):
            return other == self.listener
        return False


class EventEmitter:

    def __init__(self) -> None:
        self._events = {}

    def on(self, event, listener):
        self._on(event, ListenerWrapper(listener))

    def once(self, event, listener):
        self._on(event, ListenerWrapper(listener, is_once=True))

    def _on(self, event, listener_wrapper):
        if event not in self._events:
            self._events[event] = []
        self._events[event].append(listener_wrapper)

    def emit(self, event, *args, **kwargs):
        if event in self._events:
            # 'once' may delete items while iterating over listeners -> we use a copy
            listeners = self._events[event][:]
            for listener in listeners:
                if listener.is_once:
                    self.remove(event, listener)
                listener(*args, **kwargs)

    def remove(self, event, listener):
        if event in self._events:
            events = self._events[event]
            if listener in events:
                events.remove(listener)

    def remove_all(self, event):
        if event in self._events:
            self._events[event] = []

    def count(self, event):
        return len(self._events[event]) if event in self._events else 0


def on(emitter, event):
    def decorator(func):
        emitter.on(event, func)
        return func
    return decorator


def once(emitter, event):
    def decorator(func):
        emitter.once(event, func)
        return func
    return decorator
