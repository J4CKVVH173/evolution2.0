import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{message};\n\n\n",
            "style": "{",
        }
    },
    "handlers": {
        "genome": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "genome.log"),
            "formatter": "standard",
        },
        "info": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "info.log"),
            "formatter": "standard",
        }
    },
    "loggers": {
        "genome_logger": {"handlers": ["genome"], "level": "INFO"},
        "info_logger": {"handlers": ["info"], "level": "INFO"},
    },
}
