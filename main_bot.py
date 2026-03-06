import logging
import requests
import os
import sys
from playwright.sync_api import sync_playwright

# Professional logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

# TODO: In a production environment, use os.getenv('TELEGRAM_TOKEN')
# For this portfolio demo, we are keeping it simple.
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE" 
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

def send_telegram_alert(message: str) -> None:
    """Sends a formatted message to the connected Telegram channel."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("🔔 Notification sent to Telegram.")
        else:
            logging.warning(f"Failed to send notification: {response.text}")
    except Exception as e:
        logging.error(f"Connection error with Telegram API: {e}")

def run_automation(state_path: str) -> None:
    """
    Loads the saved session and performs the scraping task without re-login.
    """
    if not os.path.exists(state_path):
        logging.critical(f"❌ Session file '{state_path}' not found! Run auth_manager.py first.")
        sys.exit(1)

    with sync_playwright() as p:
        try:
            logging.info("Starting headless browser with persisted session...")
            browser = p.chromium.launch(headless=True)
            
            # Load the magic cookies
            context = browser.new_context(storage_state=state_path)
            page = context.new_page()

            # Go directly to the internal page
            page.goto("https://www.saucedemo.com/inventory.html")

            # Security Check: Did the session expire?
            if page.locator(".login_container").is_visible():
                logging.warning("⚠️ Session expired. Please re-authenticate.")
                return

            # --- Business Logic (Scraping) ---
            product = page.locator(".inventory_item_name").first.inner_text()
            price = page.locator(".inventory_item_price").first.inner_text()
            
            logging.info(f"Data Extracted: {product} -> {price}")

            # Send Alert
            msg = f"🚀 **Stock Alert System**\n\n📦 Item: {product}\n💰 Price: {price}\n✅ Status: Available"
            send_telegram_alert(msg)

            browser.close()
            logging.info("Process completed successfully.")

        except Exception as e:
            logging.error(f"Runtime Error: {e}")

if __name__ == "__main__":
    run_automation("auth.json")