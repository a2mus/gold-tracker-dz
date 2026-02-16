# Product Context - Gold Tracker DZ

**Created:** 2026-02-15
**Last Updated:** 2026-02-15 14:44
**Maintainer:** @mus_Doro3_bot

---

## 🇩🇿 Domain Knowledge: Algerian Gold Market

### Price Structure
- **Unit:** Prices quoted in **Algerian Dinar (DZD) per gram**
- **Karats:** 18k, 21k, 22k, 24k (purity levels)
- **Spread:** Buy prices (kassi) vs. Sell prices (mounach)

### Market Behavior
- **High frequency:** Prices change daily or multiple times per day
- **Source of truth:** Major jewelers post prices on Telegram
- **Trust factor:** Consumers track multiple jewelers for price comparison
- **Seasonality:** Demand peaks during weddings, holidays, Ramadan

### Data Sources
- **Primary:** Telegram channels of jewelers
  - Text messages with prices
  - Images of price lists (requires OCR)
  - Frequency: 1-5 posts per day per jeweler
- **Secondary:** Historical data (backfilled from past messages)

---

## 👥 User Personas

### 1. The Consumer (Amine)
- **Goal:** Know current gold prices before buying
- **Pain Point:** Calling multiple jewelers or checking scattered Telegram channels
- **Need:** Quick overview of 18k/21k prices from trusted sources
- **Device:** Mobile-first, checks on-the-go

### 2. The Jeweler (Karim)
- **Goal:** Track market movements to set competitive prices
- **Pain Point:** Manual price tracking across competitors
- **Need:** Historical trends, price charts, market intelligence
- **Device:** Desktop for analysis, mobile for updates

### 3. The Researcher (Yasmin)
- **Goal:** Study gold price patterns over time
- **Pain Point:** No centralized historical data
- **Need:** Clean, exportable data with timestamps
- **Device:** Desktop, API access

---

## 🌐 Language & Localization

- **Primary Languages:** Arabic, French (Algerian context)
- **RTL Support:** Right-to-left layout for Arabic
- **Date Format:** DD/MM/YYYY (Algerian standard)
- **Number Format:** 1,234 or 1 234 (space-separated thousands)

---

## 📱 Usage Patterns

- **Peak Hours:** 9 AM - 8 PM (shopping hours)
- **Daily Active Users:** Expected 50-200 (initial phase)
- **Core Actions:**
  1. Check today's prices (landing page)
  2. Compare jewelers (price table)
  3. View historical trends (chart)
  4. Share prices (WhatsApp/Telegram integration)

---

## ⚠️ Market Challenges

1. **Unstructured Data:** Prices buried in images and mixed text/image posts
2. **No Central API:** Jewelers don't provide structured data feeds
3. **Variability:** Different jewelers use different formats
4. **Trust:** Users need source attribution (which jeweler posted which price)

---

## 🎯 Success Metrics

- **Coverage:** Track top 10 jewelers in Algeria
- **Latency:** Prices appear on dashboard within 5 min of Telegram post
- **Accuracy:** OCR extraction >95% correct
- **Uptime:** Dashboard available 99%+ of time
- **Engagement:** 50+ daily active users by Month 2

---

*This context defines the "who" and "where" of Gold Tracker DZ. Technical implementation is in techContext.md.*
