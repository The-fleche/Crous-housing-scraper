# 🏠 CROUS Housing Notifier (August 2025)

## 📖 Project Overview
Finding student housing in France is notoriously difficult due to high demand and rapid listings turnover. I developed this **automated monitoring tool** to track the CROUS housing portal in real-time, ensuring I never miss an opening.

The script continuously monitors specific geographical bounds and sends instant desktop/system notifications as soon as a new offer is detected.

## ⚙️ Technical Architecture

### 1. Web Automation & Scraping
- **Selenium WebDriver:** Used to simulate real human behavior on the portal, handling dynamic content that standard HTTP requests often miss.
- **Headless Mode:** Configured for background execution, allowing the script to run silently on a server or local machine without interrupting work.

### 2. Anti-Bot Strategy
To avoid being flagged by anti-scraping measures, the tool implements several techniques:
- **Custom User-Agents:** Rotates/Sets realistic browser identifiers.
- **Session Management:** Uses a `requests.Session` object to maintain cookies and bypass basic automated-access restrictions.
- **Dynamic Intervals:** Implements random/fixed sleep timers to mimic human browsing patterns.

### 3. Reliability & Error Handling
Since the script is meant to run for days/weeks:
- **Auto-Restart Logic:** If the browser driver crashes or the connection drops, the script logs the error and automatically re-initializes the session.
- **Logging System:** All events (findings, errors, retries) are timestamped and logged for debugging.

## 🛠 Technologies
- **Language:** Python 3
- **Libraries:** - `Selenium` (Browser automation)
  - `Requests` (Session handling)
  - `Plyer` (System notifications)
  - `Logging` (Process tracking)

## 🧠 What I Learned
- **Bypassing Restrictions:** Understanding how websites detect bots and learning how to adjust headers and session logic to stay undetected.
- **Process Robustness:** Writing code that can survive network timeouts or site updates without manual intervention.
- **Data Extraction:** Navigating complex CSS selectors and nested HTML structures to find specific data points.

## 🚀 How to Run

1. **Prerequisites:**
   - Chrome Browser installed.
   - ChromeDriver (matched to your Chrome version).

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. Follow the explanation in the Project report

### Project report is coming soon...