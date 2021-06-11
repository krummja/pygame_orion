from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Optional

import configparser
import logging
import os
import sys

from deepmerge import always_merger

if TYPE_CHECKING:
    from configparser import ConfigParser

logger = logging.getLogger(__file__)


LIBDIR = os.path.dirname(os.path.realpath(__file__))
logger.debug("libdir: %s", LIBDIR)


USER_STORAGE_DIR = os.path.join(os.path.expanduser("~"), ".orion.d")
logger.debug("userdir: %s", USER_STORAGE_DIR)


DEFAULT_CONFIG_FILE = "orion.cfg"
USER_CONFIG_PATH = os.path.join(USER_STORAGE_DIR, DEFAULT_CONFIG_FILE)
logger.debug("user config: %s", USER_CONFIG_PATH)


DEFAULT_CONFIG = {
    "logging": {
        "loggers": "all",
        "debug_logging": True,
        "debug_level": "info",
    }
}


class OrionConfig:

    def __init__(
            self,
            options: Optional[Dict[str, Any]] = None,
            config_path: Optional[str] = None,
        ) -> None:
        if options is not None:
            config = always_merger.merge(DEFAULT_CONFIG, options)
            self.cfg = generate_config(config)
        else:
            self.cfg = generate_config()

        loggers = self.cfg.get("logging", "loggers")
        self.loggers = loggers.replace(" ", "").split(",")
        self.debug_logging = self.cfg.getboolean("logging", "debug_logging")
        self.debug_level = self.cfg.get("logging", "debug_level")

        with open(config_path if config_path else USER_CONFIG_PATH, "w") as fp:
            self.cfg.write(fp)


def generate_config(options: Optional[Dict[str, Any]] = None) -> ConfigParser:
    cfg = configparser.ConfigParser()
    populate_config(cfg, options if options else DEFAULT_CONFIG)
    return cfg


def populate_config(config: ConfigParser, data: Dict[str, Any]) -> None:
    for k, v in data.items():
        try:
            config.add_section(k)
        except configparser.DuplicateSectionError:
            pass
        for option, value in v.items():
            config.set(k, option, str(value))
