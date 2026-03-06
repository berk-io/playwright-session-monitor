import logging
from playwright.sync_api import sync_playwright

# Configure logging to look professional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

def create_session(username: str, password: str, state_path: str) -> None:
    """
    Authenticates the user on the demo platform and saves the session state.
    This demonstrates 'Login Persistence' capabilities.
    """
    with sync_playwright() as p:
        try:
            # We use headless=False to visualize the login process (optional)
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            page = context.new_page()

            logging.info("Initiating login sequence on SauceDemo...")
            page.goto("https://www.saucedemo.com/")

            logging.info(f"Authenticating user: {username}")
            page.fill("#user-name", username)
            page.fill("#password", password)
            page.click("#login-button")

            # Validate login success
            if page.locator(".inventory_list").is_visible():
                logging.info("Login successful. Verifying dashboard access...")
                
                # Save the session (cookies & local storage)
                context.storage_state(path=state_path)
                logging.info(f"✅ Session state securely saved to '{state_path}'")
            else:
                logging.error("❌ Login failed. Dashboard element not found.")

            browser.close()

        except Exception as e:
            logging.error(f"Critical error during authentication: {e}")

if __name__ == "__main__":
    # Standard credentials for the demo site
    create_session("standard_user", "secret_sauce", "auth.json")