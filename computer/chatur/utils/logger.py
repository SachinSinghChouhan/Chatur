import logging
import os
import sys
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """Setup logger with UTF-8 safe file and console handlers"""

    log_dir = Path(os.getenv('APPDATA')) / 'Computer' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 📄 File handler (UTF-8)
    file_handler = logging.FileHandler(
        log_dir / 'computer.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 🖥️ Console handler (UTF-8) - only if stdout is available
    if sys.stdout is not None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.stream.reconfigure(encoding='utf-8')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    logger.propagate = False
    return logger
