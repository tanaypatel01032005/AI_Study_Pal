import logging
import sys
from backend.app.core.config import get_settings

def setup_logger(name: str) -> logging.Logger:
    """
    Configure and return a standard logger for the application.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if the logger is already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create console handler with formatting
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        
    return logger

# Create a default logger instance
logger = setup_logger("ai_study_pal")
