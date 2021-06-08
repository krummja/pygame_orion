from pygame_orion.core.events.emitter import EventEmitter

BOOT = "BOOT"
TEARDOWN = "TEARDOWN"
PAUSE = "PAUSE"
PRE_RENDER = "PRE_RENDER"
POST_RENDER = "POST_RENDER"
PRE_STEP = "PRE_STEP"
POST_STEP = "POST_STEP"
READY = "READY"
RESUME = "RESUME"
STEP = "STEP"

__all__ = [
    "EventEmitter",
    "BOOT",
    "TEARDOWN",
    "PAUSE",
    "PRE_RENDER",
    "POST_RENDER",
    "PRE_STEP",
    "POST_STEP",
    "READY",
    "RESUME",
    "STEP"
]
