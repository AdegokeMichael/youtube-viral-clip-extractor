import logging
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "youtube_clipper",
    log_file: Optional[str] = "logs/app.log",
    level: int = logging.INFO
) -> logging.Logger:
    """
    Configures a reusable logger.
    
    Args:
        name: Logger name.
        log_file: Path to log file (None for console-only).
        level: Logging level (e.g., logging.INFO).
    
    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler (if specified)
    if log_file:
        Path(log_file).parent.mkdir(exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

if _name_ == "_main_":
    logger = setup_logger()
    logger.info("Logger test successful!")