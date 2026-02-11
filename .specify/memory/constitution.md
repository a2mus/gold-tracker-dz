# Project Constitution

## Core Principles

1. **Real Data First**: No mock data allowed in production code. All displayed prices must originate from verified scraped sources or user input.
2. **Resilient Scraping**: The scraper is the heart of the system. It must be robust, handle network failures, support multiple authentication methods (Bot/User), and fail gracefully.
3. **Context-First Development**: We rely on the `memory-bank` to track progress and context. Before starting any task, read `memory-bank/activeContext.md` and `memory-bank/projectBrief.md`. Update these files as meaningful progress is made.
4. **Docker-First Architecture**: All components (Web, API, Scraper, DB) must run in isolated Docker containers. Local environment should mirror production.
5. **Automated CI/CD**: Deployments are automated via GitHub Actions. No manual file edits on the server unless for emergency debugging.
6. **Data Integrity**: The database (TimescaleDB) is the single source of truth. Historical price data is critical and must be preserved and backed up.

## Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js 14.2, Tailwind CSS, Recharts |
| **Backend** | Python FastAPI, Pydantic, SQLAlchemy (Async) |
| **Database** | PostgreSQL 16 + TimescaleDB |
| **Scraper** | Python, Telethon (Telegram), PaddleOCR (Image Parsing) |
| **Infra** | Docker Compose, Caddy (Reverse Proxy), GitHub Actions |

## Development Standards

- **Speckit Protocol**: All new features and significant changes must follow the Speckit Protocol (Spec -> Plan -> Code -> Verify). Start with a `specs/` file.
- **Linting**: Python code follows PEP8. Typescript follows standard linting.
- **Secrets**: No secrets in code. Use `.env` and GitHub Secrets.
