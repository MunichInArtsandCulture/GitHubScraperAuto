import requests
import datetime

# Replace with your actual bot token
BOT_TOKEN = "7088435202:AAEiMKtFxJQvA3Shdcv8sQP6vGxyOKt7Ktw"

# Define group chat IDs
CHAT_IDS = ["-1002417180355", "-1002339250618"]

# Get current German time
now = datetime.datetime.now()
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
