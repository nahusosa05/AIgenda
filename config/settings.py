import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
COHERE_TOKEN = os.getenv("COHERE_TOKEN")