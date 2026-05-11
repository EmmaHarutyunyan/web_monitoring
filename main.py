import time
import csv
import random  
from urllib.parse import urlparse

from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TARGET_URL, CHECK_INTERVAL
from storage import load_seen, save_seen
from filters import is_valid
from scraper import get_page, extract_items
from notifier import send
from logger import log

def get_base(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def monitor():
    seen = load_seen()
    base_url = get_base(TARGET_URL)

    soup = get_page(TARGET_URL)
    
    if soup is None:
        print("⚠️ Warning: Scraper returned no data. Possible soft-block.")
        return 

    items = extract_items(soup, base_url)
    
    if not items:
        print(" No items matched the CSS selectors on this page.")
        return

    new_count = 0
    with open("data.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        for item in items:
            title = item["title"]
            link = item["link"]

            if not is_valid(title):
                continue

            if link in seen:
                continue

            log(f"Found: {title}")
            writer.writerow([title, link])
            save_seen(link)
            seen.add(link)
            
            send(f"🚨 NEW ITEM FOUND\n\n{title}\n\n{link}")
            new_count += 1
        
    print(f"Check finished. {new_count} new items sent.")

if __name__ == "__main__":
    print("🚀 ENTERPRISE MONITOR STARTING...")
    
    if not TARGET_URL:
        print("❌ Error: TARGET_URL not set in .env")
    else:
        while True:
            try:
                print(f"\n[{time.strftime('%H:%M:%S')}] Checking {TARGET_URL}...")
                monitor()
            except KeyboardInterrupt:
                print("\n Monitor stopped by user.")
                break
            except Exception as e:
                log(f"CRITICAL ERROR: {e}")
                print(f"Loop error: {e}")

            wait_time = CHECK_INTERVAL + random.randint(-30, 30)
            wait_time = max(10, wait_time) 
            print(f" Waiting {wait_time}s until next check...")
            time.sleep(wait_time)