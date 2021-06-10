from __future__ import annotations
from typing import Any, TYPE_CHECKING, Dict, Tuple

from deepmerge import always_merger
import pygame
import configparser
from collections import OrderedDict
from typing import Optional

from pygame_orion._constants import USER_CONFIG_PATH

if TYPE_CHECKING:
    from configparser import ConfigParser


DEFAULTS = {
    "display": {
        "fullscreen": False,
        "width": 1440,
        "height": 1080,
        "fps": 60,
        "min_fps": 30,
    },
    "gui": {},
    "game": {
        "debug": False,
    },
    "plugins": {
        "ecs": True,
        "input": True,
        "renderer": True,
        "scenes": True,
    },
    "logging": {
        "loggers": "all",
        "debug_logging": True,
        "debug_level": "info"
    }
}


class OrionConfig:

    def __init__(
            self,
            framework_config: Optional[Dict[str, Any]] = None,
            config_path: Optional[str] = None
        ) -> None:
        if framework_config is not None:
            config = always_merger.merge(DEFAULTS, framework_config)
            cfg = generate_config_from_dict(config)
        else:
            cfg = generate_default_config()

        self.cfg = cfg

        pygame.init()

        # [display]
        fullscreen = cfg.getboolean("display", "fullscreen")
        display_width = cfg.getint("display", "width")
        display_height = cfg.getint("display", "height")

        if fullscreen:
            info = pygame.display.Info()
            self.display_size = info.current_w, info.current_h
        else:
            self.display_size = display_width, display_height
        self.screen_mode = (0, pygame.FULLSCREEN)[fullscreen]
        pygame.display.set_mode(
            self.display_size,
            self.screen_mode
        )

        self.fps = cfg.getint("display", "fps")
        self.min_fps = cfg.getint("display", "min_fps")

        self.debug = cfg.getboolean("game", "debug")

        self.ecs = cfg.getboolean("plugins", "ecs")
        self.input = cfg.getboolean("plugins", "input")
        self.renderer = cfg.getboolean("plugins", "renderer")
        self.scenes = cfg.getboolean("plugins", "scenes")

        loggers = cfg.get("logging", "loggers")
        self.loggers = loggers.replace(" ", "").split(",")
        self.debug_logging = cfg.getboolean("logging", "debug_logging")
        self.debug_level = cfg.get("logging", "debug_level")

        if not config_path:
            path = USER_CONFIG_PATH
        else:
            path = config_path

        with open(path, "w") as fp:
            self.cfg.write(fp)


def generate_default_config() -> ConfigParser:
    cfg = configparser.ConfigParser()
    populate_config(cfg, DEFAULTS)
    return cfg


def generate_config_from_dict(config: Dict[str, Any]) -> ConfigParser:
    cfg = configparser.ConfigParser()
    populate_config(cfg, config)
    return cfg


def populate_config(config: ConfigParser, data: Dict[str, Any]) -> None:
    for k, v in data.items():
        try:
            config.add_section(k)
        except configparser.DuplicateSectionError:
            pass
        for option, value in v.items():
            config.set(k, option, str(value))
