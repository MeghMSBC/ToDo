# logger.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get log directory from environment or use default
LOG_DIR = os.getenv("LOG_DIR", "logs")
Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

# Filename with today's date
log_filename = os.path.join(LOG_DIR, f"todo-{datetime.now().strftime('%d-%m-%y')}.log")

# Create a timed rotating file handler (daily rotation)
handler = TimedRotatingFileHandler(log_filename, when="midnight", interval=1, backupCount=7)
handler.suffix = "%d-%m-%y"

# Set log format
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)

# Set up logger
logger = logging.getLogger("todo_logger")
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False  # Avoid duplicate logs
