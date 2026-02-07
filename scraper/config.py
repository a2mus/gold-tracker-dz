import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_ID = int(os.getenv("TELEGRAM_API_ID", "0"))
TELEGRAM_API_HASH = os.getenv("TELEGRAM_API_HASH", "")
TELEGRAM_SESSION_NAME = os.getenv("TELEGRAM_SESSION_NAME", "gold_tracker_session")
TELEGRAM_CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@bijouteriechalabi")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/gold_tracker")
