"""Logging configuration for the Taxi MDP package."""
import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """Configure logging for the package.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging output
        format_string: Optional custom format string

    Returns:
        Root logger for the package

    Example:
        >>> setup_logging(level='DEBUG', log_file='mdp.log')
        >>> logger = logging.getLogger('mdp_taxi')
        >>> logger.info('Starting solver')
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Create formatter
    formatter = logging.Formatter(format_string)

    # Get root logger for the package
    logger = logging.getLogger("mdp_taxi")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module.

    Args:
        name: Module name (will be prefixed with 'mdp_taxi.')

    Returns:
        Logger instance

    Example:
        >>> logger = get_logger('solver')
        >>> logger.info('Running value iteration')
    """
    if not name.startswith("mdp_taxi"):
        name = f"mdp_taxi.{name}"
    return logging.getLogger(name)


class LoggingContext:
    """Context manager for temporary logging configuration.

    Useful for temporarily changing logging level or output.

    Example:
        >>> with LoggingContext(level='DEBUG'):
        ...     # Debug logging enabled here
        ...     pass
        >>> # Original logging restored
    """

    def __init__(
        self,
        level: Optional[str] = None,
        log_file: Optional[str] = None
    ):
        """Initialize logging context.

        Args:
            level: Temporary logging level
            log_file: Temporary log file
        """
        self.level = level
        self.log_file = log_file
        self.logger = logging.getLogger("mdp_taxi")
        self.original_level = None
        self.original_handlers = None

    def __enter__(self):
        """Enter context and apply temporary logging settings."""
        self.original_level = self.logger.level
        self.original_handlers = self.logger.handlers.copy()

        if self.level:
            self.logger.setLevel(getattr(logging, self.level.upper()))

        if self.log_file:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore original logging settings."""
        self.logger.setLevel(self.original_level)
        self.logger.handlers = self.original_handlers
        return False
