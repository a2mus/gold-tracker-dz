# Project Constitution

## Core Principles

1. **Real Data First**: No mock data allowed in production code. All displayed prices must originate from verified scraped sources or user input.
2. **Resilient Scraping**: The scraper is the heart of the system. It must be robust, handle network failures, support multiple authentication methods (Bot/User), and fail gracefully.
3. **Docker-First Architecture**: All components (Web, API, Scraper, DB) must run in isolated Docker containers. Local environment should mirror production.
4. **Automated CI/CD**: Deployments are automated via GitHub Actions. No manual file edits on the server unless for emergency debugging.
5. **Data Integrity**: The database (TimescaleDB) is the single source of truth. Historical price data is critical and must be preserved and backed up.

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js 14, Tailwind CSS, Recharts |
| **Backend** | Python FastAPI, Pydantic |
| **Database** | PostgreSQL 16 + TimescaleDB |
| **Scraper** | Python, Telethon (Telegram), PaddleOCR (Image Parsing) |
| **Infra** | Docker Compose, Caddy (Reverse Proxy), GitHub Actions |

## Development Standards

- **Spec-Driven**: All new features start with a `spec.md` in `specs/`.
- **Linting**: Python code follows PEP8. Typescript follows standard linting.
- **Secrets**: No secrets in code. Use `.env` and GitHub Secrets.
