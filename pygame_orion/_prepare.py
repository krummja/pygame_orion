import os
import logging

from pygame_orion.core.config import OrionConfig
from pygame_orion._constants import (
    LIBDIR,
    DEFAULT_CONFIG_FILE,
    USER_STORAGE_DIR,
    USER_CONFIG_PATH
)


logger = logging.getLogger(__file__)


if not os.path.isdir(USER_STORAGE_DIR):
    os.makedirs(USER_STORAGE_DIR)
    logger.debug(f"Creating user storage directory at {USER_STORAGE_DIR}")
else:
    logger.debug(f"Found user storage directory at {USER_STORAGE_DIR}")
