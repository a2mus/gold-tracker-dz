# System Patterns - Gold Tracker DZ

**Created:** 2026-02-15
**Last Updated:** 2026-02-15 14:44
**Maintainer:** @mus_Doro3_bot

---

## 🏗️ Architecture Overview

### Pattern: Microservices with Docker Compose
```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Caddy     │──────│   Next.js   │──────│   FastAPI   │
│  (Gateway)  │      │  (Frontend) │      │    (API)    │
└─────────────┘      └─────────────┘      └─────────────┘
                            │                     │
                            │                ┌────┴────┐
                            │                │         │
                      ┌─────▼─────┐    ┌────▼──┐  ┌──▼──────┐
                      │ TimescaleDB│    │ Scraper │  │ Scraper │
                      │  (DB)      │    │  (OCR)  │  │ (Text)  │
                      └────────────┘    └─────────┘  └─────────┘
```

### Network Architecture
- **Dual-network topology:** Services on `gold-tracker-dz_default`, Gateway on `nexus-net`
- **Bridge pattern:** Web/API connected to both networks for Caddy accessibility
- **Service discovery:** Caddy resolves container names via shared Docker network

---

## 🔄 Data Flow Patterns

### 1. Ingestion Pipeline (Telegram → DB)
```
Telegram Channel → Telethon → Message Queue → OCR/Text Extraction → PostgreSQL/TimescaleDB
```
- **Pattern:** Pub/Sub (Telegram as publisher, scraper as subscriber)
- **Reliability:** Persistent sessions, auto-reconnect
- **Idempotency:** Deduplication by message ID

### 2. Query Pipeline (DB → Frontend)
```
Next.js → FastAPI → PostgreSQL/TimescaleDB → JSON Response → Frontend Rendering
```
- **Pattern:** API Gateway (FastAPI as single entry point)
- **Caching:** Response caching for expensive queries
- **Pagination:** Limit data transfer for historical queries

### 3. Gateway Routing (Caddy → Services)
```
User Request → Caddy → TLS Termination → Reverse Proxy → Container
```
- **Pattern:** Reverse Proxy with Automatic TLS (Let's Encrypt)
- **Load Balancing:** Single-instance per service (no LB needed yet)
- **Security:** Automatic HTTPS, HTTP/2 support

---

## 🎨 Design Patterns

### Scraper Pattern: Event-Driven
- **Trigger:** New Telegram message event
- **Action:** Extract → Transform → Load (ETL)
- **Error Handling:** Retry with exponential backoff
- **Fallback:** If OCR fails, store raw image for manual processing

### API Pattern: RESTful with Service Layer
- **Route Organization:**
  - `/api/prices` - Price data
  - `/api/jewelers` - Source metadata
  - `/api/history` - Time-series data
- **Validation:** Pydantic models for request/response
- **Documentation:** Auto-generated OpenAPI (Swagger UI)

### Frontend Pattern: Server-Side Rendering (Next.js)
- **Page Generation:** Static where possible, dynamic for real-time data
- **Data Fetching:** Server-side props for initial load, client-side for updates
- **State Management:** React hooks + Context API (no Redux yet)

---

## 🔒 Security Patterns

### 1. Credential Management
- **Environment Variables:** `.env` file (not in git)
- **Secrets Scope:** GitHub Container Registry (GHCR) tokens
- **Telegram Credentials:** API_ID, API_HASH stored in Docker secrets

### 2. Network Security
- **Internal Communication:** Containers communicate via Docker network (no public exposure)
- **External Exposure:** Only Caddy ports 80/443 exposed
- **Database:** No public access, only from API container

### 3. Rate Limiting (Future)
- **API:** Token bucket per IP
- **Scraper:** Respect Telegram's FloodWait (automatic backoff)

---

## 📊 State Management

### Database Schema Pattern
- **Time-Series Optimization:** TimescaleDB hypertables for `gold_prices` table
- **Indexing:** Composite index on `(jeweler_id, timestamp)`
- **Partitioning:** Monthly partitions for efficient queries

### Scraper State Pattern
- **Session Persistence:** Telethon session file stored in volume
- **Checkpointing:** Last processed message ID stored in DB
- **Recovery:** On restart, resume from last checkpoint

---

## 🚀 Deployment Patterns

### CI/CD Pipeline
```
GitHub Push → GitHub Action → Build & Push to GHCR → VPS Pull → Docker Compose Restart
```

### Blue-Green Deployment (Future)
- **Current:** Zero-downtime restarts (restart policy: always)
- **Planned:** Blue-green for rolling updates

### Monitoring (Future)
- **Logs:** Centralized logging (currently docker logs)
- **Metrics:** Prometheus + Grafana (planned)
- **Alerts:** Uptime monitoring + Slack/Telegram alerts

---

## 🧪 Testing Patterns

### Current State
- **Manual:** User testing via web browser
- **API:** Swagger UI for manual endpoint testing

### Planned
- **Unit Tests:** pytest for scraper/API
- **Integration Tests:** Test full pipeline with mock Telegram data
- **E2E Tests:** Playwright for frontend

---

*These patterns define the "how" of Gold Tracker DZ. Tech stack details are in techContext.md.*
