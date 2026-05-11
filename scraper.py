import time
import random
import undetected_chromedriver as uc
from bs4 import BeautifulSoup

import os
def get_driver():
    options = uc.ChromeOptions()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    bot_profile = os.path.join(script_dir, "bot_data")
    if not os.path.exists(bot_profile):
        os.makedirs(bot_profile)

    options.add_argument(f"--user-data-dir={bot_profile}")
    options.add_argument("--window-size=1920,1080")
    
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    options.add_argument("--lang=en-US")

    driver = uc.Chrome(options=options, version_main=147, use_subprocess=True)
    return driver

def get_page(url):
    driver = get_driver()
    if not driver: return None

    try:
        driver.execute_cdp_cmd("Network.setUserAgentOverride", {
            "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        })

        driver.get(url)
        
        time.sleep(random.randint(6, 10))
        driver.execute_script("window.scrollTo(0, 300);")
        
        print(f"DEBUG: Page Title: {driver.title}")

        if "Sorry!" in driver.title or "Robot Check" in driver.title:
            print("❌ Still blocked. Action needed: Reset your IP (Restart Router/Hotspot)")
            return None

        return BeautifulSoup(driver.page_source, "html.parser")
    except Exception as e:
        print(f"Scraper error: {e}")
        return None
    finally:
        try:
            driver.quit()
        except:
            pass

def get_page(url):
    driver = get_driver()
    if not driver:
        return None

    try:
        driver.get("https://www.google.com")
        time.sleep(random.randint(2, 4))
        
        driver.get(url)
        
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(random.randint(2, 5))
        
        print(f"DEBUG: Current Title: {driver.title}")

        if "Sorry!" in driver.title or "Robot Check" in driver.title:
            print("🛑 Amazon still blocking. Try changing your IP or URL.")
            return None

        html = driver.page_source
        return BeautifulSoup(html, "html.parser")

    except Exception as e:
        print(f"Scraper error: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def extract_items(soup, base_url):
    if not soup:
        return []
        
    items = []

    products = soup.select('div[data-component-type="s-search-result"]')
    
    print(f"🔍 Scraper found {len(products)} potential containers.")

    for p in products:
        try:
            title_tag = (
                p.select_one('h2 a span') or 
                p.select_one('h2 span') or 
                p.select_one('.a-size-medium.a-color-base.a-text-normal') or
                p.select_one('.a-size-base-plus.a-color-base.a-text-normal')
            )
            
            link_tag = p.select_one('h2 a') or p.select_one('a.a-link-normal.s-no-outline')

            if title_tag and link_tag:
                title = title_tag.text.strip()
                link = link_tag.get("href")
                
                if len(title) < 5:
                    continue

                if link.startswith("/"):
                    link = base_url + link
                
                if "ref=" in link:
                    link = link.split("ref=")[0]

                items.append({"title": title, "link": link})
        except Exception as e:
            continue
            
    print(f"🎯 Successfully extracted {len(items)} clean titles/links.")
    return items