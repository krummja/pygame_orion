import logging
import sys


def configure(config) -> None:
    """Configure logging based on the settings in the config file."""

    LOG_LEVELS = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL
    }
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
            log_handler.setFormatter(logging.Formatter(fmt = " %(name)s :: %(levelname)-8s :: %(message)s"))
            logger.addHandler(log_handler)
            loggers[logger_name] = logger
