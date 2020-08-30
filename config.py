""" Здесь хранятся все настройки """

import os
import logging

# Берём API_KET и SECRET_KEY из переменных окружения
API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Настройки базы данных
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")
PG_HOST = "127.0.0.1"
PG_PORT = "5432"

# Настройки логгера
BASE_DIR = os.path.dirname(os.path.realpath(__file__))


class InfoFilter:
    """Allow only LogRecords whose severity levels are below ERROR."""

    def __call__(self, log):
        if log.levelno == logging.INFO:
            return 1
        else:
            return 0


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "info_filter": {
            "()": InfoFilter,
        }
    },
    "formatters": {
        "info_formatter": {
            "format": "{message}",
            "style": "{",
        },
        "error_formatter": {
            "format": "{asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_info": {
            "level": logging.INFO,
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "info.log"),
            "formatter": "info_formatter",
            "filters": ["info_filter"],
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "error.log"),
            "formatter": "error_formatter",
        },
    },
    "loggers": {
        'voicekit_logger': {
            'handlers': ['file_info', 'file_error'],
            'level': 'DEBUG',
        },
    },
}


