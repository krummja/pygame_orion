import logging
import os
import sys


logger = logging.getLogger(__file__)


LIBDIR = os.path.dirname(os.path.realpath(__file__))
logger.debug("libdir: %s", LIBDIR)


USER_STORAGE_DIR = os.path.join(os.path.expanduser("~"), ".orion.d")
logger.debug("userdir: %s", USER_STORAGE_DIR)


DEFAULT_CONFIG_FILE = "orion.cfg"
USER_CONFIG_PATH = os.path.join(USER_STORAGE_DIR, DEFAULT_CONFIG_FILE)
logger.debug("user config: %s", USER_CONFIG_PATH)


__all__ = [
    "LIBDIR",
    "USER_STORAGE_DIR",
    "USER_CONFIG_PATH"
]

