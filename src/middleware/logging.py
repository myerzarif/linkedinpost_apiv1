import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from typing import Any, Dict

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)


class CustomFormatter(logging.Formatter):
    """
    Custom formatter with color coding for different log levels
    """
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: blue + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red +
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging(
    log_level: str = "INFO",
    log_file: str = "app.log",
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> Dict[str, Any]:
    """
    Setup logging configuration with both console and file handlers

    Args:
        log_level: Minimum log level to capture
        log_file: Name of the log file
        max_file_size: Maximum size of each log file in bytes
        backup_count: Number of backup files to keep

    Returns:
        Dictionary containing logger configuration
    """
    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(log_level)

    # Prevent duplicate logs
    if logger.handlers:
        logger.handlers.clear()

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    # File Handler with rotation by size
    file_handler = RotatingFileHandler(
        logs_dir / log_file,
        maxBytes=max_file_size,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Daily rotating file handler
    daily_handler = TimedRotatingFileHandler(
        logs_dir / "daily.log",
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )
    daily_handler.setFormatter(file_formatter)
    logger.addHandler(daily_handler)

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
                "level": log_level
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(logs_dir / log_file),
                "formatter": "default",
                "maxBytes": max_file_size,
                "backupCount": backup_count,
                "encoding": "utf-8",
                "level": log_level
            }
        },
        "loggers": {
            "app": {
                "level": log_level,
                "handlers": ["console", "file"],
                "propagate": False
            }
        }
    }
