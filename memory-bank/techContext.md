# Tech Context - Gold Tracker DZ

**Created:** 2026-02-15
**Last Updated:** 2026-02-15 14:44
**Maintainer:** @mus_Doro3_bot

---

## 🐳 Container Stack

### Images & Versions
| Component | Image | Version | Registry |
|-----------|-------|---------|----------|
| Frontend | `ghcr.io/a2mus/gold-tracker-dz/web` | latest | GHCR |
| API | `ghcr.io/a2mus/gold-tracker-dz/api` | latest | GHCR |
| Scraper | `ghcr.io/a2mus/gold-tracker-dz/scraper` | latest | GHCR |
| Database | `timescale/timescaledb` | latest-pg16 | Docker Hub |
| Gateway | `caddy` | latest | Docker Hub |

### Docker Compose Configuration
- **File:** `/home/mus/production/gold-tracker-dz/docker-compose.yml`
- **Networks:**
  - `gold-tracker-dz_default` (172.21.0.0/16) - Internal
  - `nexus-net` (172.18.0.0/16) - Gateway connectivity
- **Volumes:**
  - `gold_data` - PostgreSQL data persistence
  - `./scraper_sessions` - Telegram session persistence

---

## 🌐 Frontend Stack

### Core Technologies
- **Framework:** Next.js (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Charts:** Recharts or Chart.js (price visualization)
- **Deployment:** Static export + Docker container

### Environment Variables
```env
NEXT_PUBLIC_API_URL=https://gold-tracker-dz.duckdns.org
```

### Port Mapping
- **Internal:** 3000
- **External:** None (proxied via Caddy)

---

## 🔧 API Stack

### Core Technologies
- **Framework:** FastAPI (Python)
- **Database Driver:** asyncpg (PostgreSQL)
- **ORM:** SQLAlchemy (async)
- **Validation:** Pydantic
- **Documentation:** OpenAPI/Swagger (auto-generated)

### Endpoints
- **Root:** `GET /` - Health check
- **Docs:** `GET /docs` - Swagger UI
- **Prices:** `GET /api/prices` - Current prices
- **History:** `GET /api/history` - Time-series data
- **Jewelers:** `GET /api/jewelers` - Source list

### Environment Variables
```env
DATABASE_URL=postgresql://goldtracker:password@db:5432/goldtracker
```

### Port Mapping
- **Internal:** 8000
- **External:** None (proxied via Caddy)

---

## 🤖 Scraper Stack

### Core Technologies
- **Telegram Client:** Telethon (Python)
- **OCR Engine:** PaddleOCR (Chinese/Arabic/English support)
- **Image Processing:** OpenCV
- **Database:** asyncpg (direct PostgreSQL writes)

### Scraping Logic
1. **Listen:** Subscribe to Telegram channels
2. **Detect:** Identify messages with prices (text + images)
3. **Extract:**
   - Text: Regex patterns for price extraction
   - Images: OCR with PaddleOCR
4. **Store:** Insert into `gold_prices` table
5. **Retry:** Failed extractions logged for manual review

### Environment Variables
```env
TELEGRAM_API_ID=******
TELEGRAM_API_HASH=******
TELEGRAM_PHONE=+213*******
TELEGRAM_SESSION_NAME=/app/sessions/gold_tracker_session
DATABASE_URL=postgresql://goldtracker:password@db:5432/goldtracker
```

### Special Features
- **Historical Sync:** Script to backfill 3 years of data
- **Rate Limiting:** Respect Telegram FloodWait automatically
- **Session Persistence:** Survives container restarts

---

## 🗄️ Database Stack

### Technology
- **Database:** PostgreSQL 16 (via TimescaleDB)
- **Extension:** TimescaleDB (time-series optimization)

### Schema (Key Tables)
```sql
gold_prices (hypertable)
  - id: BIGINT (PK)
  - jeweler_id: INTEGER
  - karat: INTEGER (18, 21, 22, 24)
  - price_buy: NUMERIC (purchase price)
  - price_sell: NUMERIC (selling price)
  - timestamp: TIMESTAMPTZ
  - source_url: TEXT (Telegram message link)
  - extraction_method: TEXT (ocr/text)

jewelers
  - id: INTEGER (PK)
  - name: TEXT
  - telegram_channel: TEXT
  - is_active: BOOLEAN
```

### Optimizations
- **Hypertable:** Partitioned by time (1 month chunks)
- **Indexes:** `(jeweler_id, timestamp)`, `karat`
- **Compression:** TimescaleDB compression for old data

---

## 🌐 Gateway Stack (Caddy)

### Configuration File
- **Location:** `/home/mus/infrastructure/Caddyfile` (shared across projects)
- **Route:** `gold-tracker-dz.duckdns.org`

### Routing Rules
```
gold-tracker-dz.duckdns.org {
  handle /api/* {
    reverse_proxy gold-tracker-api:8000
  }

  handle {
    reverse_proxy gold-tracker-web:3000
  }
}
```

### TLS Configuration
- **Provider:** Let's Encrypt (automatic)
- **Protocol:** HTTP/2, TLS 1.3
- **Certificates:** Auto-renewed by Caddy

---

## 🔐 Security Stack

### Secrets Management
- **Storage:** Environment variables in `.env` file (not in git)
- **Scope:** GitHub Container Registry (read-only token)
- **Access:** VPS only (no local secrets)

### Network Security
- **Firewall:** UFW (ports 80, 443 open only)
- **Internal Traffic:** Docker network isolation
- **Database:** No public access

---

## 🛠️ Development Tools

### Version Control
- **Repository:** https://github.com/a2mus/gold-tracker-dz
- **Branch Strategy:** `main` (production), `dev` (staging)

### CI/CD
- **Platform:** GitHub Actions
- **Triggers:** Push to `main`, Pull Request
- **Pipeline:** Build → Test → Push to GHCR → Deploy to VPS

### Monitoring
- **Logs:** `docker logs <container>`
- **Status:** Manual checks (currently)
- **Uptime:** Planned (UptimeRobot or similar)

---

## 📦 Dependencies (Key)

### Python (API/Scraper)
- `telethon` - Telegram client
- `paddleocr` - OCR engine
- `fastapi` - API framework
- `asyncpg` - PostgreSQL driver
- `uvicorn` - ASGI server

### Node.js (Frontend)
- `next` - React framework
- `tailwindcss` - Styling
- `recharts` - Charting
- `axios` - HTTP client

---

## 🚫 Technical Constraints

1. **No External APIs:** All data from Telegram (no paid APIs)
2. **Algeria-Only:** Timezone (Africa/Algiers), Currency (DZD)
3. **Single Language:** Arabic/French (no English in UI initially)
4. **Mobile-First:** Design for mobile screens first
5. **Lightweight:** Optimize for slow 3G/4G connections

---

*This context defines the "what" of Gold Tracker DZ's tech stack. Architecture patterns are in systemPatterns.md.*
