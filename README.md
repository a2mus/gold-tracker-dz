# 🥇 Algeria Gold Tracker

**Real-time gold prices for the Algerian market**

Track local gold prices (18k, 21k, 22k, 24k) from Telegram sources, compare with international rates, and get price alerts.

## Features

- 📊 Real-time Sabika (lingot) prices in DZD
- 📈 Historical price charts
- 🌍 Algeria vs World price comparison (premium indicator)
- 🔔 Telegram bot alerts for price changes
- 📱 Mobile-friendly dashboard

## Tech Stack

| Component | Technology |
|-----------|------------|
| Scraper | Python + Telethon |
| OCR | PaddleOCR |
| Backend | FastAPI |
| Database | PostgreSQL + TimescaleDB |
| Frontend | Next.js 14 |
| Deployment | Docker + GitHub Actions |

## Project Structure

```
gold-tracker-dz/
├── scraper/           # Telegram scraper (Python)
│   ├── src/
│   ├── requirements.txt
│   └── Dockerfile
├── api/               # FastAPI backend
│   ├── src/
│   ├── requirements.txt
│   └── Dockerfile
├── web/               # Next.js frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── bot/               # Telegram alert bot
│   ├── src/
│   └── Dockerfile
├── docker-compose.yml
├── docker-compose.prod.yml
└── .github/workflows/
    └── deploy.yml
```

## Environment Variables

```env
# Telegram API (from my.telegram.org)
TELEGRAM_API_ID=
TELEGRAM_API_HASH=
TELEGRAM_PHONE=

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/goldtracker

# Bot
BOT_TOKEN=
```

## Development

```bash
# Clone
git clone https://github.com/a2mus/gold-tracker-dz.git
cd gold-tracker-dz

# Start services
docker-compose up -d

# View logs
docker-compose logs -f scraper
```

## Deployment

Automatically deployed to VPS via GitHub Actions on push to `main`.

**Production URL:** https://gold.nexus-dz.com

---

*Part of the Nexus-DZ Labs portfolio*
