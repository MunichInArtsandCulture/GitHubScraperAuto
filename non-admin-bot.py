import requests

TOKEN = "7604302798:AAEhQIp2rYVngyX-aMK4jIVY3vt1L4QzAfQ"
CHAT_ID = "-1002274858775"
MESSAGE = "https://www.youtube.com/watch?v=NusqkPMxq0g"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": MESSAGE}

response = requests.post(url, data=data)

print(response.json())
