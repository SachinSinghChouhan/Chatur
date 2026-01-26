"""Logging utility"""

import logging
from pathlib import Path
import os

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with file handler"""
    log_dir = Path(os.getenv('APPDATA')) / 'Computer' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # File handler
    handler = logging.FileHandler(log_dir / 'computer.log')
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    # Console handler
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)
    
    return logger
