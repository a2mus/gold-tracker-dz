
import asyncio
import os
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import tempfile
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

# Import from local files
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_SESSION_NAME,
    TELEGRAM_CHANNEL,
    DATABASE_URL
)
from db.models import GoldMarketData, MarketBrief, CurrencySnapshot, RiskAlert, Base
from paddleocr import PaddleOCR

# Setup Async DB
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ar')

# Note: Using sub-agent for AI parsing since the local gemini CLI is disabled
from sessions_spawn import sessions_spawn

PARSING_PROMPT = """
You are an expert in the Algerian gold market. Parse this Telegram update into JSON.
GOLD MARKET RULES:
1. "يساك" or "كاسي" = Used gold.
2. "تكسير" = Broken/scrap.
3. "750" = 18k.
4. "999" = 24k.
5. Brands like INNOVA, SADE, MONACO = Imported.
Return ONLY valid JSON.
"""

async def parse_with_ai_agent(text, ocr_text):
    task = f"{PARSING_PROMPT}\n\nTEXT:\n{text}\n\nOCR:\n{ocr_text}"
    result = await sessions_spawn(
        task=task,
        label="gold-parser",
        model="google-antigravity/gemini-3-flash",
        thinking="low"
    )
    
    # Simple extraction logic for sub-agent result
    raw = result['announcement']
    if "```json" in raw:
        raw = raw.split("```json")[1].split("```")[0].strip()
    elif "```" in raw:
        raw = raw.split("```")[1].strip()
    
    if "Run finished:" in raw:
        raw = raw.split("Run finished:")[1].strip()
        
    return json.loads(raw)

async def run_scraper(limit=5):
    client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    
    print(f"Scraping {limit} messages from {TELEGRAM_CHANNEL}...")
    
    async with AsyncSessionLocal() as db:
        async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=limit):
            ocr_text = ""
            if message.media and isinstance(message.media, MessageMediaPhoto):
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                    await client.download_media(message.media, tmp.name)
                    res = ocr.ocr(tmp.name, cls=True)
                    if res and res[0]:
                        ocr_text = '\n'.join([line[1][0] for line in res[0]])
                    os.unlink(tmp.name)
            
            if not message.text and not ocr_text:
                continue
                
            print(f"Parsing message {message.id}...")
            parsed = await parse_with_ai_agent(message.text or "", ocr_text)
            
            if not parsed:
                continue
                
            # Save Market Data
            for item in parsed.get('market_data', []):
                record = GoldMarketData(
                    timestamp=message.date.replace(tzinfo=None),
                    karat=item['karat'],
                    gold_type=item['gold_type'],
                    condition=item['condition'],
                    origin=item['origin'],
                    price_min=item['price_min'],
                    price_max=item.get('price_max'),
                    message_id=message.id
                )
                db.add(record)
            
            # Save Market Brief
            brief_data = parsed.get('market_brief')
            if brief_data:
                brief = MarketBrief(
                    timestamp=message.date.replace(tzinfo=None),
                    global_spot_usd=brief_data.get('global_spot_usd'),
                    sentiment=brief_data.get('sentiment'),
                    ai_summary=brief_data.get('ai_summary'),
                    raw_analysis=message.text,
                    key_events=brief_data.get('key_events'),
                    message_id=message.id
                )
                db.add(brief)
                
            # Save Currency
            curr = parsed.get('currency')
            if curr and (curr.get('usd_buy') or curr.get('eur_buy')):
                snapshot = CurrencySnapshot(
                    timestamp=message.date.replace(tzinfo=None),
                    usd_buy=curr.get('usd_buy'),
                    eur_buy=curr.get('eur_buy'),
                    message_id=message.id
                )
                db.add(snapshot)
                
            await db.commit()
            print(f"  Saved data for {message.date}")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(run_scraper())
