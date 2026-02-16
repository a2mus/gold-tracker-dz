# Gold Tracker DZ - Project Memory Bank

**Project:** gold-tracker-dz  
**Topic:** DOROS #80 (Development Discussions)  
**Memory Bank Maintainer:** @mus_Doro3_bot  
**Last Updated:** 2026-02-15 14:13 (Confirmed Online)

---

## 📋 Project Overview

Gold Tracker DZ is a real-time gold price tracking platform for the Algerian market. It scrapes Telegram channels from major jewelers, extracts price data using OCR (PaddleOCR), and presents it through a web dashboard.

**Public URL:** https://gold-tracker-dz.duckdns.org/

---

## 🏗️ Architecture

### Components
| Component | Technology | Status |
|-----------|------------|--------|
| Frontend | Next.js | Running on port 3000 |
| API | FastAPI | Running on port 8000 |
| Scraper | Python + Telethon + PaddleOCR | Active |
| Database | PostgreSQL + TimescaleDB | Healthy |
| Gateway | Caddy | Handling SSL + routing |

### Network Configuration
- **Internal Network:** `gold-tracker-dz_default` (172.21.0.0/16)
- **Gateway Network:** `nexus-net` (172.18.0.0/16)
- **Note:** Web and API containers are connected to both networks for Caddy accessibility

---

## 🚀 Deployment Status

**Current State:** ✅ ONLINE

### Containers (as of 2026-02-15)
- ✅ `gold-tracker-db` - Healthy
- ✅ `gold-tracker-api` - Responding
- ✅ `gold-tracker-web` - Accessible (with intermittent errors)
- ✅ `gold-tracker-scraper` - Active, syncing historical data
- ✅ `caddy` - Routing traffic

### Recent Fixes
- **2026-02-15:** Fixed 502 Bad Gateway by connecting web/API containers to `nexus-net`
- **2026-02-15:** Restarted Caddy to pick up network changes

---

## ⚠️ Known Issues

1. **Frontend Errors:** Next.js showing `TypeError: ... reading 'digest'` in logs
2. **Domain:** `gold.nexus-dz.com` configured in Caddy but DNS not set up (NXDOMAIN)
3. **Historical Sync:** Scraper is backfilling data from Feb 2026 backward (ETA: ~6 hours)

---

## 📝 Decision Log

### 2026-02-15
- **Topic 80 created** exclusively for gold-tracker-dz development discussions
- **Role assignment:** @mus_clawd_bot (Boss), @mus_Doro2_bot (Implementation), @mus_Doro3_bot (Research/Memory)
- **Issue:** Website not accessible via `gold-tracker-dz.duckdns.org`
- **Root Cause:** Network isolation - Caddy couldn't resolve `gold-tracker-web`
- **Solution:** Connected containers to `nexus-net` and restarted Caddy
- **Result:** Website now accessible
- **Confirmed:** @attmus verified website is online and accessible (14:13 GMT+1)

---

## 🔧 Technical Notes

### Docker Commands Reference
```bash
# View logs
docker logs --tail 20 gold-tracker-web
docker logs --tail 20 gold-tracker-api
docker logs --tail 20 gold-tracker-scraper
docker logs --tail 20 caddy

# Restart services
docker restart caddy
docker restart gold-tracker-web

# Network troubleshooting
docker network inspect gold-tracker-dz_default
docker network inspect nexus-net
```

### API Endpoints
- API Docs: `https://gold-tracker-dz.duckdns.org/api/docs`
- Health Check: `https://gold-tracker-dz.duckdns.org/`

---

## 📊 Data Pipeline

1. **Scraper** listens to Telegram channels
2. **OCR** extracts prices from images (PaddleOCR)
3. **Data** stored in TimescaleDB
4. **API** serves data to frontend
5. **Frontend** displays charts and current prices

---

## 🎯 Next Actions (Pending)

- [ ] Monitor frontend stability (investigate digest errors)
- [ ] Verify historical sync completion
- [ ] Assess data quality in dashboard
- [ ] Remove `gold.nexus-dz.com` from Caddy config (or set up DNS)

---

*This memory bank is maintained by @mus_Doro3_bot. Updates are made based on conversations in DOROS topic #80.*
