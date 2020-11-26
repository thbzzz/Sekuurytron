import logging
import logging.config

import colorlog

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "consoleFormatter": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s[%(asctime)s] %(levelname)s => %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "colorlog.StreamHandler",
            "formatter": "consoleFormatter",
        },
    },
    "loggers": {
        "logger": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
})

log = logging.getLogger("logger")
log.setLevel(logging.DEBUG)
