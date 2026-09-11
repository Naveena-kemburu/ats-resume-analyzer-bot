import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
TEMP_DIR = str(BASE_DIR / 'temp')

# Ensure temp directory exists
os.makedirs(TEMP_DIR, exist_ok=True)
