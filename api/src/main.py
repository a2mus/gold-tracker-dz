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
    
    if not db_pool:
        raise HTTPException(status_code=503, detail="Database not available")
    
    async with db_pool.acquire() as conn:
        # Get latest prices from view
        latest = await conn.fetch("""
            SELECT karat, current_price, last_updated
            FROM latest_gold_prices
            ORDER BY karat
        """)
        
        if not latest:
            # Return empty if no data
            return []
        
        # Get 24h ago prices for comparison
        yesterday = datetime.utcnow() - timedelta(hours=24)
        
        prices = []
        for row in latest:
            karat = row['karat']
            current = float(row['current_price'])
            last_updated = row['last_updated']
            
            # Get 24h stats
            stats = await conn.fetchrow("""
                SELECT 
                    AVG((buy_price + sell_price) / 2) AS avg_24h,
                    MIN((buy_price + sell_price) / 2) AS low_24h,
                    MAX((buy_price + sell_price) / 2) AS high_24h
                FROM gold_prices
                WHERE karat = $1
                  AND timestamp >= $2
            """, karat, yesterday)
            
            avg_24h = float(stats['avg_24h'] or current)
            low_24h = float(stats['low_24h'] or current)
            high_24h = float(stats['high_24h'] or current)
            
            change_24h = current - avg_24h
            change_percent = (change_24h / avg_24h * 100) if avg_24h > 0 else 0
            
            prices.append(PriceSummary(
                karat=karat,
                current_price=round(current, 2),
                change_24h=round(change_24h, 2),
                change_percent=round(change_percent, 2),
                high_24h=round(high_24h, 2),
                low_24h=round(low_24h, 2),
                last_updated=last_updated
            ))
        
        return prices


@app.get("/api/v1/prices/history", response_model=List[dict], tags=["Prices"])
async def get_price_history(
    karat: Optional[int] = Query(None, description="Filter by gold karat"),
    days: int = Query(30, description="Number of days", ge=1, le=365),
    granularity: str = Query("daily", description="daily or hourly")
):
    """Get historical prices with daily or hourly granularity"""
    
    if not db_pool:
        raise HTTPException(status_code=503, detail="Database not available")
    
    async with db_pool.acquire() as conn:
        if granularity == "hourly" and days <= 7:
            # Use hourly data for last 7 days
            view_name = "gold_prices_hourly"
            date_col = "hour"
        else:
            # Use daily data for longer periods
            view_name = "historical_gold_prices_daily"
            date_col = "date"
        
        query = f"""
            SELECT 
                {date_col} AS timestamp,
                karat,
                avg_price,
                data_points
            FROM {view_name}
            WHERE timestamp >= NOW() - INTERVAL '{days} days'
        """
        
        if karat:
            query += f" AND karat = {karat}"
        
        query += f" ORDER BY timestamp DESC, karat"
        
        rows = await conn.fetch(query)
        
        return [
            {
                "timestamp": row['timestamp'].isoformat(),
                "karat": row['karat'],
                "avg_price": float(row['avg_price']),
                "data_points": row['data_points']
            }
            for row in rows
        ]


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
