"""
Enhanced Database models for Gold Intelligence System.
Uses SQLAlchemy with async support for PostgreSQL/TimescaleDB.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Index, Text, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GoldMarketData(Base):
    """Granular gold price records."""
    __tablename__ = 'gold_market_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    karat = Column(String(5), nullable=False)  # 18k, 21k, 24k, 750, 999
    gold_type = Column(String(50))             # Jewelry, Bar, Coin, Scrap
    condition = Column(String(50))            # New, Used (Kassi), Broken (Taksir)
    origin = Column(String(50))               # Local, Imported, BrandName (Innova, etc.)
    price_min = Column(Float, nullable=False)
    price_max = Column(Float)                 # Optional for ranges
    currency = Column(String(10), default='DZD')
    message_id = Column(Integer)
    
    __table_args__ = (
        Index('idx_gold_market_ts', 'timestamp'),
        Index('idx_gold_market_karat_type', 'karat', 'gold_type'),
    )

class MarketBrief(Base):
    """Market analysis and global context."""
    __tablename__ = 'market_briefs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    global_spot_usd = Column(Float)           # USD/oz spot price
    sentiment = Column(Text)                  # Bullish, Bearish, Neutral, Correction
    ai_summary = Column(Text)                 # 1-sentence AI summary
    raw_analysis = Column(Text)               # Original Arabic text analysis
    key_events = Column(JSON)                 # List of events (e.g., ["US Labor Data 11 Feb"])
    message_id = Column(Integer)

class CurrencySnapshot(Base):
    """Parallel market currency rates."""
    __tablename__ = 'currency_snapshots'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    usd_buy = Column(Float)
    usd_sell = Column(Float)
    eur_buy = Column(Float)
    eur_sell = Column(Float)
    message_id = Column(Integer)

class RiskAlert(Base):
    """Expert-defined risk thresholds."""
    __tablename__ = 'risk_alerts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    karat = Column(String(5))
    threshold_price = Column(Float)
    alert_type = Column(String(50))           # "Purity Warning", "Scam Alert"
    description = Column(Text)
    message_id = Column(Integer)
