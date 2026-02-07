# Gold Tracker DZ 🪙

Real-time Algerian gold price tracking via Telegram channel scraping.

**Target:** https://gold.nexus-dz.com

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Telegram      │────▶│   Scraper       │────▶│   PostgreSQL    │
│   @bijouterie   │     │   (Telethon +   │     │   TimescaleDB   │
│   chalabi       │     │   PaddleOCR)    │     │                 │
└─────────────────┘     └─────────────────┘     └────────┬────────┘
                                                         │
                        ┌─────────────────┐              │
                        │   Next.js       │◀─────────────┤
                        │   RTL Dashboard │              │
                        │   (Arabic)      │     ┌────────┴────────┐
                        └─────────────────┘     │   FastAPI       │
                                                │   REST API      │
                                                └─────────────────┘
```

## Stack

- **Scraper:** Python + Telethon + PaddleOCR
- **Backend:** FastAPI + SQLAlchemy
- **Database:** PostgreSQL + TimescaleDB
- **Frontend:** Next.js 14 + RTL Arabic UI

## Setup

### 1. Environment
```bash
cp .env.example .env
# Edit .env with your Telegram credentials
```

### 2. Install Dependencies
```bash
# Python backend
pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

### 3. Database
```bash
# Create database
createdb gold_tracker

# Run migrations
alembic upgrade head

# Enable TimescaleDB (optional, for better time-series performance)
psql gold_tracker -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

### 4. First Run (Telegram Auth)
```bash
cd scraper
python telegram_scraper.py
# Follow prompts to authenticate with Telegram
```

### 5. Run Services
```bash
# API
uvicorn api.main:app --reload

# Frontend
cd frontend && npm run dev
```

## Deployment

Target: Contabo VPS with Caddy reverse proxy

```
gold.nexus-dz.com → Caddy → :3000 (Next.js)
gold.nexus-dz.com/api → Caddy → :8000 (FastAPI)
```

## Price Sources

- **Primary:** @bijouteriechalabi (Telegram)
- **Format:** Daily posts with 18k, 21k, 22k, 24k prices in DZD/gram

## License

MIT
