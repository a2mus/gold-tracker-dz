
import asyncio
import json
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add scraper directory to path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'scraper'))
from config import DATABASE_URL
from models import GoldMarketData, MarketBrief, CurrencySnapshot, RiskAlert

# Setup Async DB
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def import_parsed_data():
    json_path = '/home/mus/production/gold-tracker-dz/scraper/parsed_history.json'
    with open(json_path, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    async with AsyncSessionLocal() as db:
        for entry in dataset:
            dt = datetime.fromisoformat(entry['date']).replace(tzinfo=None)
            msg_id = entry['message_id']
            
            # 1. Market Data
            for item in entry.get('market_data', []):
                db.add(GoldMarketData(
                    timestamp=dt,
                    karat=item['karat'],
                    gold_type=item['gold_type'],
                    condition=item['condition'],
                    origin=item['origin'],
                    price_min=item['price_min'],
                    price_max=item.get('price_max'),
                    message_id=msg_id
                ))
            
            # 2. Market Brief
            brief_data = entry.get('market_brief')
            if brief_data:
                db.add(MarketBrief(
                    timestamp=dt,
                    global_spot_usd=brief_data.get('global_spot_usd'),
                    sentiment=brief_data.get('sentiment'),
                    ai_summary=brief_data.get('ai_summary'),
                    key_events=brief_data.get('key_events'),
                    message_id=msg_id
                ))
            
            # 3. Currency
            curr = entry.get('currency')
            if curr and (curr.get('usd_buy') or curr.get('eur_buy')):
                db.add(CurrencySnapshot(
                    timestamp=dt,
                    usd_buy=curr.get('usd_buy'),
                    eur_buy=curr.get('eur_buy'),
                    message_id=msg_id
                ))
            
            # 4. Risk Alerts
            for alert in entry.get('risk_alerts', []):
                db.add(RiskAlert(
                    timestamp=dt,
                    karat=alert.get('karat'),
                    threshold_price=alert.get('threshold'),
                    description=alert.get('description'),
                    message_id=msg_id
                ))
        
        await db.commit()
        print(f"Imported {len(dataset)} entries into database.")

if __name__ == "__main__":
    asyncio.run(import_parsed_data())
