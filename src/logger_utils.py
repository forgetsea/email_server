import logging
from pathlib import Path
from .config import LOG_FILE

LOGS_DIR = Path('./logs')
LOGS_DIR.mkdir(exist_ok=True)

def get_logger():
    logger = logging.getLogger('email_sender')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():  # 防止重复添加 Handler
        logger.addHandler(file_handler)

    return logger

logger = get_logger()
