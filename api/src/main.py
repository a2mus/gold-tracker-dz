"""
FastAPI Backend for Gold Tracker
Provides API endpoints for gold price data
"""

from datetime import datetime, timedelta
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import asyncpg

# Database connection pool
db_pool: Optional[asyncpg.Pool] = None


# Pydantic models
class GoldPriceResponse(BaseModel):
    """Gold price data point"""
    id: int
    timestamp: datetime
    karat: int = Field(..., description="Gold karat (18, 21, 22, 24)")
    buy_price: Optional[float] = Field(None, description="Buy price in DZD")
    sell_price: Optional[float] = Field(None, description="Sell price in DZD")
    source: str = Field(..., description="Data source")


class PriceSummary(BaseModel):
    """Price summary for a karat"""
    karat: int
    current_price: float
    change_24h: Optional[float]
    change_percent: Optional[float]
    high_24h: Optional[float]
    low_24h: Optional[float]
    last_updated: datetime


class WorldPrice(BaseModel):
    """International gold price"""
    price_usd: float
    price_dzd: float
    premium_percent: float


class DashboardData(BaseModel):
    """Main dashboard data"""
    prices: List[PriceSummary]
    world_price: WorldPrice
    last_update: datetime


# Lifespan for database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage database connection pool lifecycle"""
    global db_pool
    
    import os
    database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/goldtracker')
    
    try:
        db_pool = await asyncpg.create_pool(database_url, min_size=2, max_size=10)
        yield
    finally:
        if db_pool:
            await db_pool.close()


# Create FastAPI app
app = FastAPI(
    title="Algeria Gold Tracker API",
    description="Real-time gold prices for the Algerian market",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Gold Tracker API",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/api/v1/prices/current", response_model=List[PriceSummary], tags=["Prices"])
async def get_current_prices():
    """Get current prices for all karats"""
    
    # Mock data for initial development
    # TODO: Replace with database queries
    now = datetime.utcnow()
    
    return [
        PriceSummary(
            karat=18,
            current_price=29700,
            change_24h=100,
            change_percent=0.34,
            high_24h=29800,
            low_24h=29500,
            last_updated=now
        ),
        PriceSummary(
            karat=21,
            current_price=34650,
            change_24h=150,
            change_percent=0.43,
            high_24h=34800,
            low_24h=34400,
            last_updated=now
        ),
        PriceSummary(
            karat=22,
            current_price=36300,
            change_24h=200,
            change_percent=0.55,
            high_24h=36500,
            low_24h=36000,
            last_updated=now
        ),
        PriceSummary(
            karat=24,
            current_price=39600,
            change_24h=250,
            change_percent=0.63,
            high_24h=39800,
            low_24h=39300,
            last_updated=now
        ),
    ]


@app.get("/api/v1/prices/history", response_model=List[GoldPriceResponse], tags=["Prices"])
async def get_price_history(
    karat: int = Query(18, description="Gold karat"),
    days: int = Query(7, description="Number of days", ge=1, le=365)
):
    """Get historical prices for a specific karat"""
    
    # Mock data
    # TODO: Replace with database queries
    now = datetime.utcnow()
    history = []
    
    base_prices = {18: 29700, 21: 34650, 22: 36300, 24: 39600}
    base = base_prices.get(karat, 29700)
    
    for i in range(days * 4):  # 4 data points per day
        timestamp = now - timedelta(hours=i * 6)
        variation = (i % 10 - 5) * 50  # Simple variation
        
        history.append(GoldPriceResponse(
            id=i,
            timestamp=timestamp,
            karat=karat,
            buy_price=base + variation,
            sell_price=base + variation + 200,
            source="mock"
        ))
    
    return history


@app.get("/api/v1/prices/world", response_model=WorldPrice, tags=["Prices"])
async def get_world_price():
    """Get international gold price comparison"""
    
    # TODO: Fetch from external API (goldrate24.com, etc.)
    return WorldPrice(
        price_usd=2850.50,
        price_dzd=39600,
        premium_percent=2.3  # Algeria premium over world price
    )


@app.get("/api/v1/dashboard", response_model=DashboardData, tags=["Dashboard"])
async def get_dashboard_data():
    """Get all data for the dashboard"""
    
    prices = await get_current_prices()
    world = await get_world_price()
    
    return DashboardData(
        prices=prices,
        world_price=world,
        last_update=datetime.utcnow()
    )


@app.get("/api/v1/alerts/subscribe", tags=["Alerts"])
async def subscribe_alerts(
    karat: int = Query(18),
    threshold: float = Query(..., description="Price threshold in DZD"),
    direction: str = Query("above", description="'above' or 'below'"),
    telegram_user_id: str = Query(..., description="Telegram user ID for notifications")
):
    """Subscribe to price alerts"""
    
    # TODO: Implement alert subscription
    return {
        "status": "subscribed",
        "karat": karat,
        "threshold": threshold,
        "direction": direction,
        "telegram_user_id": telegram_user_id
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
