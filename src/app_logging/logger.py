
from __future__ import annotations

import logging
from pathlib import Path


def get_app_logger(
    name: str = "future_leaders_ai",
    log_path: str = "data/cache/app.log",
) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def log_event(message: str, **kwargs):
    logger = get_app_logger()
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.info(f"{message} {extra}".strip())


def log_error(message: str, error: Exception | str | None = None, **kwargs):
    logger = get_app_logger()
    extra = " ".join(f"{k}={v}" for k, v in kwargs.items())
    if error:
        logger.error(f"{message} error={error} {extra}".strip())
    else:
        logger.error(f"{message} {extra}".strip())
