import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN_2") or os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID_2") or os.getenv("TELEGRAM_CHAT_ID", "-1002274858775")
MESSAGE = "https://www.youtube.com/watch?v=NusqkPMxq0g"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.post(url, data=data)

print(response.json())
