# 🏠 CROUS Housing Notifier (August 2025)

## 📖 Project Overview
Finding student housing in France is notoriously difficult due to high demand and rapid listings turnover. I developed this **automated monitoring tool** to track the CROUS housing portal in real-time, ensuring I never miss an opening.

The script continuously monitors specific geographical bounds and sends instant desktop/system notifications as soon as a new offer is detected.

> 📑 **Looking for the full technical analysis?** [Read the Project Report (PDF)](./rapport_scraper.pdf)


## ⚙️ Technical Architecture

### 1. Web Automation & Scraping
- **Selenium WebDriver:** Used to simulate real human behavior on the portal, handling dynamic content that standard HTTP requests (like BeautifulSoup alone) often miss.
- **Headless Mode:** Configured for background execution, allowing the script to run silently on a server or local machine without interrupting work.

### 2. Anti-Bot Strategy & Session Management
To avoid being flagged by anti-scraping measures, the tool implements several techniques:
- **Custom User-Agents:** Mimics realistic browser identifiers to stay undetected.
- **Session Persistence:** Uses browser cookies to maintain an active connection and bypass basic automated-access restrictions.
- **Dynamic Intervals:** Implements sleep timers to mimic human browsing patterns and avoid server-side rate limiting.

### 3. Reliability & Error Handling
Since the script is designed to run autonomously for weeks (e.g., during holidays):
- **Auto-Restart Logic:** If the browser driver crashes or the connection drops, the script logs the error and automatically re-initializes a new session.
- **Logging System:** All events (findings, errors, retries) are timestamped and logged in a local `.log` file for debugging.
- **ntfy Integration:** Uses the ntfy API to send real-time alerts directly to a mobile device, ensuring high reactivity even when away from the computer.

## 🛠 Technologies
- **Language:** Python 3
- **Main Libraries:** - `Selenium` (Browser automation)
  - `Requests` (Session handling & API calls)
  - `Plyer` (Desktop notifications)
  - `Logging` (Process tracking)

## 🧠 What I Learned
- **Bypassing Restrictions:** Understanding how websites detect bots and learning how to adjust headers, cookies, and session logic.
- **Process Robustness:** Writing "resilient" code that can survive network timeouts or driver crashes without manual intervention.
- **Data Extraction:** Navigating complex CSS selectors and nested HTML structures to find specific data points.

## 🚀 How to Run

1. **Prerequisites:**
   - Chrome Browser installed.
   - ChromeDriver (matched to your Chrome version).

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration**: 
   - Update the local file paths (logs, drivers) in the script comments.
   - Provide your CROUS session cookies as indicated in the code.

4. **Detailed Instructions**:
   - Refer to the Project Report for a step-by-step setup guid

## 📂 Repository Structure

- `Crous notifier.py`: Final script
- `Logement_checker.py`: First script attempt with static approach
- `rapport_scraper.pdf`: Project report
