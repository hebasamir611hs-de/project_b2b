"""
Logger - Centralized logging utility with colored console output.
"""

import logging
import sys
from typing import Optional
from pathlib import Path

from config.settings import Settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter with ANSI colors for console output."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format log record with colors."""
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


class Logger:
    """
    Centralized logger for the application.
    Implements Singleton pattern to ensure single logger instance.
    """
    
    _instance: Optional[logging.Logger] = None
    _initialized: bool = False
    
    @classmethod
    def get_logger(cls, name: str = None) -> logging.Logger:
        """
        Get or create logger instance.
        
        Args:
            name: Logger name (default from settings)
        
        Returns:
            Logger instance
        """
        if cls._instance is not None and cls._initialized:
            return cls._instance
        
        if name is None:
            name = Settings.PROJECT_NAME
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, Settings.LOG_LEVEL))
        logger.handlers.clear()
        logger.propagate = False
        
        # Console handler with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = ColoredFormatter(
            Settings.LOG_FORMAT,
            Settings.LOG_DATE_FORMAT
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler (if enabled)
        if Settings.LOG_TO_FILE:
            try:
                # Ensure logs directory exists
                Settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(
                    Settings.LOG_FILE_NAME,
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_formatter = logging.Formatter(
                    Settings.LOG_FORMAT,
                    Settings.LOG_DATE_FORMAT
                )
                file_handler.setFormatter(file_formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                logger.warning(f"Could not create file handler: {str(e)}")
        
        cls._instance = logger
        cls._initialized = True
        
        return logger
    
    @classmethod
    def reset(cls) -> None:
        """Reset logger instance (useful for testing)."""
        if cls._instance:
            for handler in cls._instance.handlers[:]:
                handler.close()
                cls._instance.removeHandler(handler)
        cls._instance = None
        cls._initialized = False
