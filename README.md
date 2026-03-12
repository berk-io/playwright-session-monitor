# 🔐 Playwright Session Persistence Engine

### Enterprise-Grade Authentication & Monitoring Architecture 

This project demonstrates a robust **"Login-Once, Run-Forever"** architecture using Python and Playwright. It solves the common problem of repetitive logins and strict rate-limiting by separating the **Authentication Phase** from the **Operational Phase**.

**Designed for:** High-security platforms requiring 2FA, Captcha handling, or complex session management (e.g., Fintech dashboards, SaaS platforms).

---

### 🏗️ Architecture

The system is split into two specialized modules to ensure stability and modularity:

| Module | Responsibility | Key Feature |
| --- | --- | --- |
| **`auth_manager.py`** | Handles login, MFA, and Captcha challenges. | Generates a serialized Session State (`auth.json`). |
| **`main_bot.py`** | Performs data extraction & monitoring. | Runs **Headless** using the pre-saved session. No re-login required. |

### 🚀 Key Features

* **Session Persistence:** Saves Cookies & LocalStorage to bypass login screens on subsequent runs.
* **Headless Execution:** Optimized for server environments (Ubuntu/VPS).
* **Error Resilience:** Checks for session expiration and alerts if re-authentication is needed.
* **Notification System:** Integrated Telegram API for real-time alerts.
* **Professional Logging:** Detailed timestamped logs instead of `print()` statements.

### 🛠️ Installation & Usage

1. **Install Dependencies:**
```bash
pip install playwright requests
playwright install

```


2. **Phase 1: Authentication (GUI Mode)**
Run the manager to perform the initial login. The browser will open for manual/automated entry.
```bash
python auth_manager.py

```


*Result: A secure `auth.json` file is generated.*
3. **Phase 2: Automation (Headless Mode)**
Run the bot. It will inject the session and start monitoring immediately.
```bash
python main_bot.py

```



---

**Disclaimer:** This repository uses `saucedemo.com` as a stable testing ground to demonstrate the architectural pattern. The logic is fully scalable to complex targets like Binance, LinkedIn, or Instagram.
