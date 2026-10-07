import os
import requests
import datetime
from pytz import timezone
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Get bot token from environment or GitHub secret
BOT_TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Error: BOT_TOKEN / TELEGRAM_BOT_TOKEN environment variable is not set!")

# Define group chat IDs
CHAT_IDS = ["-1002417180355", "-1002339250618"]

# Get current German time (CEST/MEZ)
berlin = timezone("Europe/Berlin")
now = datetime.datetime.now(berlin)
formatted_time = now.strftime("%H:%M %d/%m/%Y")

# Message to send
message = (
    f"<code>The </code>"
    f"<a href='https://t.me/munichinartsandculture/10'>job list</a>"
    f"<code> was updated at {formatted_time}</code>"
)

# Telegram API URL
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Send request to each group
for chat_id in CHAT_IDS:
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    response = requests.post(url, data=data)
    print(response.json())  # Print response (optional)
