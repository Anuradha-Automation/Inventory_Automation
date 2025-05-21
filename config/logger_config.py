import logging
from logging.handlers import RotatingFileHandler
from config.config import LOG_FILE


def setup_logger(log_level="INFO"):
    """Sets up the logger with a rotating file handler and stream handler."""
    
    logger = logging.getLogger(__name__)

    # Prevent duplicate handlers if the function is called multiple times
    if logger.hasHandlers():
        return logger

    # Set log level dynamically (case insensitive)
    log_level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level)

    # File Handler with Rotation
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Stream Handler for Console Logs
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

    # Add Handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Logging setup complete.")
    return logger