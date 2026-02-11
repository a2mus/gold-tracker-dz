# Implementation Plan - Feature 001

## Technical Approach

### 1. Unified Scraper Architecture
Split the scraper into two distinct modules running in the same container:
- **Live Listener (`live.py`)**: Uses Telethon + Bot API to listen for *new* messages.
- **Historical Backfiller (`backfill.py`)**: Uses `aiohttp` to scrape `t.me/s/channel` web preview, bypassing Bot API history restrictions.

### 2. Historical Backfill Strategy (Web Scraping)
- **Target**: `https://t.me/s/{channel_handle}`
- **Pagination**: The web preview supports `?before={message_id}` parameter.
- **Logic**:
  1. Fetch landing page.
  2. Parse messages and extract the oldest message ID.
  3. If oldest message date > 30 days ago, fetch `?before={oldest_id}`.
  4. Repeat until date limit reached.

### 3. Container Management
- **Entrypoint**: A script that runs the `live.py` listener in the foreground.
- **Cron/One-off**: The `backfill.py` script can be triggered manually or via a cron schedule inside the container (or just run once on deployment).

## Files to Create/Update

1. `scraper/requirements.txt`: Add `beautifulsoup4` (for reliable HTML parsing).
2. `scraper/src/live.py`: Refactored `scraper.py` focused purely on real-time updates.
3. `scraper/src/backfill.py`: New web-scraping implementation with pagination.
4. `scraper/src/main.py`: Supervisor script or entrypoint.

## Complexity Risks
- **Web Preview Layout Changes**: Telegram might change class names. *Mitigation*: Use loose regex or CSS selectors if possible.
- **Rate Limiting**: Telegram might block IP for too many web requests. *Mitigation*: Add `sleep(2)` between pagination requests.
