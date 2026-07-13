import logging
import os
from config import CONFIG

def setup_loggers() -> None:
    """Configures separate log files for application, embeddings, and errors."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Application Log
    app_handler = logging.FileHandler(os.path.join(CONFIG.logs_dir, 'application.log'))
    app_handler.setFormatter(formatter)
    
    # Error Log
    error_handler = logging.FileHandler(os.path.join(CONFIG.logs_dir, 'error.log'))
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # Embedding Log
    embed_logger = logging.getLogger('embedding')
    embed_handler = logging.FileHandler(os.path.join(CONFIG.logs_dir, 'embedding.log'))
    embed_handler.setFormatter(formatter)
    embed_logger.addHandler(embed_handler)
    embed_logger.setLevel(logging.INFO)

    # Attach to root
    if not root_logger.handlers:
        root_logger.addHandler(app_handler)
        root_logger.addHandler(error_handler)

setup_loggers()
logger = logging.getLogger("App")
embed_logger = logging.getLogger("embedding")