import logging
import os
from datetime import datetime

from app.config import settings

# Buat direktori logs jika belum ada
if not os.path.exists("logs"):
    os.makedirs("logs")

# Konfigurasi logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)