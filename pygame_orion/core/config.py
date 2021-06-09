from __future__ import annotations
from typing import Any, TYPE_CHECKING

import pygame
import configparser
from collections import OrderedDict
from typing import Optional

if TYPE_CHECKING:
    from configparser import ConfigParser


class OrionConfig:

    def __init__(
            self,
            config_path: Optional[str] = None
        ) -> None:
        cfg = generate_default_config()
        self.cfg = cfg

        if config_path:
            temp = configparser.ConfigParser()
            temp.read(config_path)
            populate_config(cfg, temp._sections)

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


def get_defaults() -> OrderedDict[str, Any]:
    return OrderedDict(
        (
            (
                "display",
                OrderedDict(
                    (
                        ("fullscreen", True),
                        ("width", 1440),
                        ("height", 1080),
                        ("fps", 60),
                        ("min_fps", 30),
                    )
                )
            ),
            (
                "input",
                OrderedDict(
                    (
                        ("command_keys", {}),
                        ("move_keys", {}),
                    )
                )
            )
        )
    )


def generate_default_config() -> ConfigParser:
    cfg = configparser.ConfigParser()
    populate_config(cfg, get_defaults())
    return cfg


def populate_config(config: ConfigParser, data: OrderedDict[str, Any]) -> None:
    for k, v in data.items():
        try:
            config.add_section(k)
        except configparser.DuplicateSectionError:
            pass
        for option, value in v.items():
            config.set(k, option, str(value))
