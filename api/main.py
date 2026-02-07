"""
FastAPI backend for Gold Tracker DZ.
Provides REST endpoints for gold price data.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Gold Tracker DZ API",
    description="Real-time Algerian gold price tracking",
    version="1.0.0",
)

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Models ---

class PricePoint(BaseModel):
    timestamp: datetime
    karat: str
    price_dzd: float


class CurrentPrices(BaseModel):
    timestamp: datetime
    prices: dict[str, float]  # {18k: 13900, 21k: 16200, ...}
    change_24h: dict[str, float]  # Percentage change


class PriceHistory(BaseModel):
    karat: str
    data: list[PricePoint]


# --- Mock Data (replace with DB queries) ---

MOCK_PRICES = {
    '24k': 18500,
    '22k': 17000,
    '21k': 16200,
    '18k': 13900,
}

MOCK_CHANGES = {
    '24k': 0.5,
    '22k': 0.3,
    '21k': 0.4,
    '18k': 0.2,
}


# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "ok", "service": "Gold Tracker DZ API"}


@app.get("/api/prices/current", response_model=CurrentPrices)
async def get_current_prices():
    """Get the latest gold prices for all karat levels."""
    return CurrentPrices(
        timestamp=datetime.now(),
        prices=MOCK_PRICES,
        change_24h=MOCK_CHANGES,
    )


@app.get("/api/prices/history/{karat}")
async def get_price_history(
    karat: str,
    days: int = Query(default=30, ge=1, le=365),
):
    """Get historical prices for a specific karat level."""
    if karat not in ['18k', '21k', '22k', '24k']:
        raise HTTPException(status_code=400, detail="Invalid karat level")
    
    # Generate mock history
    now = datetime.now()
    base_price = MOCK_PRICES[karat]
    
    data = []
    for i in range(days):
        date = now - timedelta(days=days - i - 1)
        # Add some variation
        price = base_price + (i % 10 - 5) * 50
        data.append(PricePoint(timestamp=date, karat=karat, price_dzd=price))
    
    return {"karat": karat, "data": data}


@app.get("/api/prices/compare")
async def compare_karats(
    days: int = Query(default=7, ge=1, le=30),
):
    """Compare all karat levels over time."""
    now = datetime.now()
    
    result = {}
    for karat, base_price in MOCK_PRICES.items():
        data = []
        for i in range(days):
            date = now - timedelta(days=days - i - 1)
            price = base_price + (i % 5 - 2) * 30
            data.append({"date": date.isoformat(), "price": price})
        result[karat] = data
    
    return result


@app.get("/api/stats")
async def get_stats():
    """Get price statistics (high, low, avg over periods)."""
    return {
        "daily": {
            "high": {"24k": 18600, "21k": 16300},
            "low": {"24k": 18400, "21k": 16100},
        },
        "weekly": {
            "high": {"24k": 18800, "21k": 16500},
            "low": {"24k": 18200, "21k": 16000},
            "change_pct": {"24k": 1.2, "21k": 0.8},
        },
        "monthly": {
            "high": {"24k": 19200, "21k": 17000},
            "low": {"24k": 17800, "21k": 15500},
            "change_pct": {"24k": 3.5, "21k": 2.9},
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
