import time
import csv
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from config import CHECK_TIME, HEADERS

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
URL = os.getenv("TARGET_URL")

CSV_FILE = "storage.csv"
SEEN_FILE = "seen.txt"


# ---------------- TELEGRAM ----------------
def send_msg(text):
    api = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(api, data=data)


# ---------------- LOAD SEEN ----------------
def load_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(f.read().splitlines())


def save_seen(item):
    with open(SEEN_FILE, "a") as f:
        f.write(item + "\n")


# ---------------- SAVE CSV ----------------
def save_csv(title, link):
    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["title", "link"])
        writer.writerow([title, link])


# ---------------- SCRAPER ----------------
def get_items():
    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    items = []

    for box in soup.select("a"):
        title = box.text.strip()
        link = box.get("href")

        if title and link and len(title) > 10:
            if not link.startswith("http"):
                link = URL + link

            items.append((title, link))

    return items


# ---------------- MAIN LOOP ----------------
def run():
    print("BOT STARTED...")

    seen = load_seen()

    while True:
        try:
            items = get_items()

            for title, link in items:
                if link not in seen:

                    print("NEW:", title[:40])

                    save_csv(title, link)
                    send_msg(f"🚨 NEW ITEM\n\n{title}\n{link}")

                    save_seen(link)
                    seen.add(link)

            print("Checked website... sleeping")

        except Exception as e:
            print("ERROR:", e)

        time.sleep(CHECK_TIME)


run()