import logging
import sys
from pathlib import Path
from typing import Optional, Any, Dict
from chatur.utils.platform import get_app_data_dir

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with UTF-8 safe file and console handlers"""

    log_dir = get_app_data_dir() / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = logging.FileHandler(
        log_dir / 'computer.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if sys.stdout is not None:
        console_handler = logging.StreamHandler(sys.stdout)
        # reconfigure is only available on TextIOWrapper (not all stdout types)
        try:
            if hasattr(console_handler.stream, 'reconfigure'):
                console_handler.stream.reconfigure(encoding='utf-8') # type: ignore
        except AttributeError:
            pass
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger


class LogContext:
    """Context manager for structured logging with extra context"""
    
    def __init__(self, logger: logging.Logger, level: int = logging.INFO, **context: Any):
        self.logger = logger
        self.level = level
        self.context = context
        self._extra: Dict[str, Any] = {}
    
    def __enter__(self) -> 'LogContext':
        for key, value in self.context.items():
            self._extra[key] = value
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is not None:
            self.logger.error(
                f"Error in context: {self.context}",
                exc_info=(exc_type, exc_val, exc_tb),
                extra=self._extra
            )
        for key in self.context:
            self._extra.pop(key, None)
    
    def debug(self, msg: str) -> None:
        self.logger.debug(msg, extra=self._extra)
    
    def info(self, msg: str) -> None:
        self.logger.info(msg, extra=self._extra)
    
    def warning(self, msg: str) -> None:
        self.logger.warning(msg, extra=self._extra)
    
    def error(self, msg: str) -> None:
        self.logger.error(msg, extra=self._extra)


def log_execution(logger: logging.Logger, operation: str) -> Any:
    """Decorator-like context manager for logging function execution"""
    class ExecutionContext:
        def __init__(self, log: logging.Logger, op: str):
            self.log = log
            self.op = op
        
        def __enter__(self):
            self.log.info(f"Starting: {self.op}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if exc_type is not None:
                self.log.error(f"Failed: {self.op} - {exc_val}", exc_info=True)
            else:
                self.log.info(f"Completed: {self.op}")
    
    return ExecutionContext(logger, operation)
