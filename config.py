import os
from dotenv import load_dotenv

load_dotenv()  # carrega .env

COINCAP_API_KEY = os.getenv("COINCAP_API_KEY")
DB_URL           = os.getenv("DB_URL")
PAGE_SIZE        = int(os.getenv("PAGE_SIZE", 100))