import os
from pygame_orion.core.config import OrionConfig
from pygame_orion._constants import (
    LIBDIR,
    DEFAULT_CONFIG_FILE,
    USER_STORAGE_DIR,
    USER_CONFIG_PATH
)


if not os.path.isdir(USER_STORAGE_DIR):
    os.makedirs(USER_STORAGE_DIR)


CONFIG = OrionConfig(USER_CONFIG_PATH)
with open(USER_CONFIG_PATH, "w") as fp:
    CONFIG.cfg.write(fp)
