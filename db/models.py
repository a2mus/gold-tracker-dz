"""
Database models for gold price storage.
Uses SQLAlchemy with async support for PostgreSQL/TimescaleDB.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, String, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GoldPrice(Base):
    """Gold price record."""
    __tablename__ = 'gold_prices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    karat = Column(String(3), nullable=False)  # 18k, 21k, 22k, 24k
    price_dzd = Column(Float, nullable=False)  # Price per gram in DZD
    source = Column(String(50), default='telegram')  # Source channel/method
    message_id = Column(Integer, nullable=True)  # Telegram message ID
    
    __table_args__ = (
        Index('idx_gold_prices_timestamp', 'timestamp'),
        Index('idx_gold_prices_karat_timestamp', 'karat', 'timestamp'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'karat': self.karat,
            'price_dzd': self.price_dzd,
            'source': self.source,
        }


class PriceSummary(Base):
    """Daily price summary (aggregated)."""
    __tablename__ = 'price_summaries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    karat = Column(String(3), nullable=False)
    open_price = Column(Float)
    close_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    avg_price = Column(Float)
    
    __table_args__ = (
        Index('idx_price_summary_date_karat', 'date', 'karat', unique=True),
    )


# TimescaleDB hypertable creation SQL (run manually or via migration)
TIMESCALE_SETUP = """
-- Convert to hypertable for time-series optimization
SELECT create_hypertable('gold_prices', 'timestamp', if_not_exists => TRUE);

-- Add compression policy (compress data older than 7 days)
ALTER TABLE gold_prices SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'karat'
);
SELECT add_compression_policy('gold_prices', INTERVAL '7 days', if_not_exists => TRUE);

-- Continuous aggregate for daily summaries
CREATE MATERIALIZED VIEW IF NOT EXISTS daily_gold_prices
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', timestamp) AS day,
    karat,
    first(price_dzd, timestamp) AS open_price,
    last(price_dzd, timestamp) AS close_price,
    max(price_dzd) AS high_price,
    min(price_dzd) AS low_price,
    avg(price_dzd) AS avg_price
FROM gold_prices
GROUP BY day, karat;
"""
