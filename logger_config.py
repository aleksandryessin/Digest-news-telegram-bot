import logging
import sys
from datetime import datetime

def setup_logging(log_level=logging.INFO):
    """Setup structured logging for the bot."""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    
    # File handler (optional, for Docker logs)
    try:
        file_handler = logging.FileHandler('/app/logs/bot.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        handlers = [console_handler, file_handler]
    except:
        # If can't write to file, just use console
        handlers = [console_handler]
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=handlers,
        force=True
    )
    
    # Set specific logger levels
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    
    return logging.getLogger('ai_digest_bot')

def get_logger(name):
    """Get a logger with the given name."""
    return logging.getLogger(name) 