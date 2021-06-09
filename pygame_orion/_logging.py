import logging
import sys
from pygame_orion import _prepare as prepare


def configure() -> None:
    """Configure logging based on the settings in the config file."""

    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
    config = prepare.CONFIG
    loggers = {}

    if config.debug_level in LOG_LEVELS:
        log_level = LOG_LEVELS[config.debug_level]
    else:
        log_level = logging.INFO

    if config.debug_logging:
        for logger_name in config.loggers:
            if logger_name == "all":
                print("Enabling logging of all modules.")
                logger = logging.getLogger()
            else:
                print("Enabling logging for module: %s" % logger_name)
                logger = logging.getLogger(logger_name)

            logger.setLevel(log_level)
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setLevel(log_level)
            log_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - " "%(levelname)s - %(message)s"))
            logger.addHandler(log_handler)
            loggers[logger_name] = logger
