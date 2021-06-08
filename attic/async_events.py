from __future__ import annotations
from typing import TYPE_CHECKING, Optional

import asyncio
import collections
import contextlib
import functools
import itertools
import warnings
from collections.abc import AsyncIterator, AsyncIterable

if TYPE_CHECKING:
    from asyncio import AbstractEventLoop


async def _try_catch_coro(emitter: EventEmitter, event, listener, coro):
    try:
        await coro
    except Exception as exc:
        if event == emitter.LISTENER_ERROR_EVENT:
            raise
        emitter.emit(emitter.LISTENER_ERROR_EVENT, event, listener, exc)


class EventEmitter:

    DEFAULT_MAX_LISTENERS: int = 10
    LISTENER_ERROR_EVENT = 'listener_error'

    def __init__(self, loop: Optional[AbstractEventLoop] = None) -> None:
        self._loop = loop or asyncio.get_event_loop()
        self._listeners = collections.defaultdict(list)
        self._once = collections.defaultdict(list)
        self._max_listeners = self.DEFAULT_MAX_LISTENERS

    def _check_limit(self, event):
        if self.count(event) > self.max_listeners:
            warnings.warn(f'Too many listeners for event {event}', ResourceWarning)

    def add_listener(self, event, listener):
        self.emit('new_listener', event, listener)
        self._listeners[event].append(listener)
        self._check_limit(event)
        return self

    def on(self, event, listener):
        return self.add_listener(event, listener)

    def once(self, event, listener):
        self.emit('new_listener', event, listener)
        self._once[event].append(listener)
        self._check_limit(event)
        return self

    def remove_listener(self, event, listener):
        with contextlib.suppress(ValueError):
            self._listeners[event].remove(listener)
            return True
        with contextlib.suppress(ValueError):
            self._once[event].remove(listener)
            return True
        return False

    def remove_all_listeners(self, event=None):
        if not event:
            self._listeners = collections.defaultdict(list)
            self._once = collections.defaultdict(list)
        else:
            del self._listeners[event]
            del self._once[event]

    @property
    def max_listeners(self):
        return self._max_listeners

    @max_listeners.setter
    def max_listeners(self, value):
        self._max_listeners = value

    def listeners(self, event):
        return self._listeners[event][:] + self._once[event][:]

    def _dispatch_coroutine(self, event, listener, *args, **kwargs):
        try:
            coro = listener(*args, **kwargs)
        except Exception as exc:
            if event == self.LISTENER_ERROR_EVENT:
                raise
            return self.emit(self.LISTENER_ERROR_EVENT, event, listener, exc)

        asyncio.ensure_future(
            _try_catch_coro(self, event, listener, coro),
            loop = self._loop
        )

    def _dispatch_function(self, event, listener, *args, **kwargs):
        try:
            return listener(*args, **kwargs)
        except Exception as exc:
            if event == self.LISTENER_ERROR_EVENT:
                raise
            return self.emit(self.LISTENER_ERROR_EVENT, event, listener, exc)

    def _dispatch(self, event, listener, *args, **kwargs):
        if (
            asyncio.iscoroutinefunction(listener) or
            isinstance(listener, functools.partial) and
            asyncio.iscoroutinefunction(listener.func)
        ):
            return self._dispatch_coroutine(event, listener, *args, **kwargs)
        return self._dispatch_function(event, listener, *args, **kwargs)

    def emit(self, event, *args, **kwargs):
        listeners = self._listeners[event]
        listeners = itertools.chain(listeners, self._once[event])
        self._once[event] = []
        for listener in listeners:
            self._loop.call_soon(
                functools.partial(
                    self._dispatch,
                    event,
                    listener,
                    *args,
                    **kwargs
                )
            )
        return self

    def count(self, event) -> int:
        return len(self._listeners[event]) + len(self._once[event])


class EventIterator:

    def __init__(self, emitter, event) -> None:
        self._emitter = emitter
        self._event = event
        self._emitter.on(event, self._push)
        self._data = collections.deque()
        self._future = None

    async def _push(self, *args, **kwargs):
        self._data.append((args, kwargs))
        if self._future:
            future, self._future = self._future, None
            future.set_result(True)

    async def __anext__(self):
        # If data... return it
        if self._data:
            return self._data.popleft()

        self._future = asyncio.Future()
        await self._future
        return self._data.popleft()


class EventIterable:

    def __init__(self, emitter, event):
        self._emitter = emitter
        self._event = event

    async def __aiter__(self) -> EventIterator:
        return EventIterator(self._emitter, self._event)
