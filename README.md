# Web Enterprise Monitor

### DESCRIPTION
Enterprise Monitor is an automated system that scans Amazon for new product listings and sends instant alerts to Telegram. It is designed with resilience and anti-detection mechanisms to ensure stable and continuous monitoring.

### KEY FEATURES
- **Robust Scraping:** Uses `undetected-chromedriver` with randomized delays to maintain a human-like footprint.
- **Smart Filtering:** Customizable system that sends alerts only for items matching your specific keywords.
- **Duplicate Prevention:** Utilizes `seen.csv` to track history and avoid repeated notifications for the same product.
- **Auto Recovery:** Built-in handling for network fluctuations and website layout changes.

### PROJECT STRUCTURE
- `main.py` — Main execution loop and error handling.
- `scraper.py` — Web scraping engine and data extraction logic.
- `filters.py` — Keyword validation and filtering system.
- `notifier.py` — Telegram bot notification service.
- `storage.py` — CSV-based storage management for tracking seen items.

### INSTALLATION

1. **Clone the repository:**
   ```bash
   git clone https://github.com/EmmaHarutyunyan/web_monitoring.git
   cd web_monitoring
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### CONFIGURATION

Create a `.env` file in the root directory:
```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
TARGET_URL=https://www.amazon.com/s?k=sneakers
CHECK_INTERVAL=300
```

### USAGE

Run the project:
```bash
python main.py
```

### NOTES
- **Compatibility:** Ensure your ChromeDriver version matches your installed Chrome browser.
- **Persistence:** Keep `seen.csv` in the project root to ensure the monitor remembers processed items.
- **Customization:** Modify `filters.py` to adjust the keyword logic for your specific Amazon search targets.



