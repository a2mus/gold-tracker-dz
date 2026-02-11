# Feature Spec 001: Robust Scraper System

## Context
The current scraper implementation is fragile. It crashes on authentication failures, lacks historical data backfilling capabilities, and struggles with container lifecycle management (exits immediately). We need a robust, "always-on" system that guarantees data ingestion.

## User Stories

- **US1**: As a system, I want to scrape historical gold prices (last 30 days) from public Telegram channels so that the dashboard shows trend charts.
- **US2**: As a system, I want to listen for new messages in real-time so that prices are updated immediately.
- **US3**: As a developer, I want the scraper to use Bot Token authentication for public channels to avoid unstable user-session requirements.
- **US4**: As a system, I want to fallback to Web Preview scraping if API access is restricted for history fetching.
- **US5**: As a system, I want to extract prices from both text and images (OCR) to maximize data coverage.

## Requirements

### Functional
- **FR1**: Scraper must support `TELEGRAM_BOT_TOKEN` for authentication.
- **FR2**: Historical backfill must parse at least 30 days of messages.
- **FR3**: Image processing (OCR) must identify price tables in images.
- **FR4**: Data must be de-duplicated using `(timestamp, karat, source)` constraint.

### Non-Functional
- **NFR1**: Container must automatically restart on failure (unless fatal config error).
- **NFR2**: Logging must be verbose enough to diagnose parsing failures.
- **NFR3**: Bot should handle rate limits gracefully.

## Technical Constraints
- **Telegram Bot API**: Cannot fetch history of channels it hasn't joined. 
  - *Mitigation*: Use Web Preview Parsing (`t.me/s/channel`) for history backfill.
- **VPS Resources**: OCR is heavy. Process images sequentially, not in parallel.

## Success Metrics
- 30 days of historical data populated in DB.
- New messages appear in DB within 1 minute.
- Scraper container uptime > 99%.
