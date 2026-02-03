"""### FILE: datalens/logger_config.py"""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


def setup_logging(log_dir: Path, log_level: int = logging.INFO) -> logging.Logger:
    """Configure and return a project logger."""
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "insight_mapping.log"

    logger = logging.getLogger("insight_mapping")
    logger.setLevel(log_level)
    logger.propagate = False

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        file_handler = RotatingFileHandler(
            log_path, maxBytes=2_000_000, backupCount=3, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
