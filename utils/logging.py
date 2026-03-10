import logging
import time

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configures a standardized logger format."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(handler)
        
    return logger

class Profiler:
    """Simple context manager for profiling code blocks."""
    def __init__(self, name: str, logger: logging.Logger = None):
        self.name = name
        self.logger = logger or setup_logger("Profiler")
        self.start_time = 0.0
        
    def __enter__(self):
        self.start_time = time.time()
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = time.time() - self.start_time
        self.logger.info(f"[{self.name}] took {duration:.4f} seconds.")
