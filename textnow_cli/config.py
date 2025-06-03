import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# TextNow credentials
USERNAME = os.getenv("TEXTNOW_USERNAME")
SID_COOKIE = os.getenv("TEXTNOW_SID_COOKIE")
CSRF_TOKEN = os.getenv("TEXTNOW_CSRF_TOKEN")

# OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API Configuration
BASE_URL = "https://www.textnow.com/api"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36" 