import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send(msg):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram credentials missing in .env")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": msg}
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Telegram notification failed: {e}")