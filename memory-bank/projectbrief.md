# Project Brief - Gold Tracker DZ

**Created:** 2026-02-15
**Last Updated:** 2026-02-15 14:44
**Maintainer:** @mus_Doro3_bot

---

## 🎯 Project Purpose

Gold Tracker DZ is a real-time financial intelligence platform for the Algerian gold market. It transforms unstructured Telegram updates from major jewelers into structured, actionable market data.

**Core Problem:** Algerian gold prices are scattered across Telegram channels in images and unstructured text, making it difficult for consumers and traders to track market movements.

**Our Solution:** Automated scraping + OCR extraction + Web dashboard for real-time price visualization.

---

## 📊 Project Scope

### In Scope
- ✅ Scraping Telegram channels (major jewelers)
- ✅ OCR-based price extraction from images (PaddleOCR)
- ✅ Real-time price updates (18k, 21k, 22k, 24k karats)
- ✅ Historical price tracking and charts
- ✅ Web dashboard for data visualization
- ✅ API for data access

### Out of Scope (Current Phase)
- ❌ Mobile app (planned for Phase 2)
- ❌ Price predictions/forecasting (future feature)
- ❌ Multi-country support (Algeria-only for now)
- ❌ Payment integration (not a marketplace)
- ❌ User authentication (public dashboard only)

---

## 🎯 Primary Goals

1. **Reliability:** 99%+ uptime for price updates
2. **Accuracy:** Minimize OCR extraction errors
3. **Speed:** Real-time updates within 5 minutes of Telegram posts
4. **Accessibility:** Public access via web dashboard
5. **Data Quality:** Maintain clean, structured historical data

---

## 👥 Target Users

- **Consumers:** People buying gold jewelry (know current prices)
- **Traders:** Jewelers tracking market movements
- **Analysts:** Researchers studying gold price trends

---

## 🚫 Non-Goals

- Not a marketplace (no buying/selling)
- Not a prediction platform (historical data only)
- Not a social network (no user accounts/comments)
- Not multi-asset (gold only, no silver/other metals)

---

*This brief defines the "why" and "what" of Gold Tracker DZ. Technical details are in techContext.md and systemPatterns.md.*
