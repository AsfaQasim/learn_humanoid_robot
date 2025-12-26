"""
Logging configuration for the RAG ingestion pipeline.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """
    Set up logging configuration for the application.

    Args:
        log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
    """
    # Create logger
    logger = logging.getLogger('rag_ingestion_pipeline')
    logger.setLevel(getattr(logging, log_level.upper()))

    # Prevent adding multiple handlers if logger already configured
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level.upper()))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Add file handler if log_file specified
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Global logger instance
logger = setup_logging()