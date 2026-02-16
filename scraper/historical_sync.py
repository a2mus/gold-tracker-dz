"""
Historical synchronization script for Algeria Gold Tracker.
Iterates through Telegram channel month-by-month, going back 3 years.
Pauses 10 minutes between months to avoid rate limiting.
"""

import os
import asyncio
import logging
import asyncpg
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import tempfile

# Add parent directory to sys.path to allow imports from sibling files
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_CHANNEL,
)
from ocr_extractor import extract_prices_from_image, extract_prices_from_text

# Use the specific session path where we have the authenticated session
SESSION_PATH = os.path.join('/home/mus/production/gold-tracker-dz/scraper_sessions', 'gold_tracker_session')
DATABASE_URL = "postgresql://goldtracker:goldtracker2026@localhost:5432/goldtracker"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def save_to_db(pool, records):
    """Save parsed gold prices to the database."""
    async with pool.acquire() as conn:
        async with conn.transaction():
            for rec in records:
                # records are list of {date, karat, price, source, text, message_id}
                await conn.execute('''
                    INSERT INTO gold_prices (timestamp, karat, sell_price, buy_price, source, raw_text, message_id, gold_type)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (timestamp, karat, source) DO UPDATE 
                    SET sell_price = EXCLUDED.sell_price,
                        raw_text = EXCLUDED.raw_text,
                        message_id = EXCLUDED.message_id
                ''', rec['date'], rec['karat'], rec['price'], rec['price'], 'telegram', rec['text'], rec['message_id'], 'new')

async def process_month(client, pool, start_date, end_date):
    """Process a single month range."""
    logger.info(f"--- Starting sync for range: {start_date.date()} to {end_date.date()} ---")
    records = []
    
    # Iterate through messages in the date range
    async for message in client.iter_messages(TELEGRAM_CHANNEL, offset_date=end_date):
        if message.date < start_date:
            break
            
        prices = {}
        # Try text extraction
        if message.text:
            prices = extract_prices_from_text(message.text)
        
        # If no prices in text and has image, try OCR
        if not prices and message.media and isinstance(message.media, MessageMediaPhoto):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                try:
                    await client.download_media(message.media, tmp.name)
                    prices = extract_prices_from_image(tmp.name)
                except Exception as e:
                    logger.error(f"Error downloading/OCR for msg {message.id}: {e}")
                finally:
                    if os.path.exists(tmp.name):
                        os.unlink(tmp.name)
        
        if prices:
            logger.info(f"Found prices at {message.date}: {prices}")
            for karat_str, price in prices.items():
                # Extract numeric karat (e.g., '18k' -> 18)
                karat = int(re.sub(r'[^\d]', '', karat_str))
                records.append({
                    'date': message.date,
                    'karat': karat,
                    'price': float(price),
                    'text': message.text or "[Image Only]",
                    'message_id': message.id
                })
    
    if records:
        logger.info(f"Saving {len(records)} records to database...")
        await save_to_db(pool, records)
        logger.info(f"Sync complete for {start_date.strftime('%B %Y')}")
    else:
        logger.info(f"No gold prices found for {start_date.strftime('%B %Y')}")

async def main():
    # Initialize DB pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    
    # Initialize Telegram client
    client = TelegramClient(SESSION_PATH, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    
    logger.info("Connection successful. Starting historical synchronization (3 years)...")
    
    # Start from current month (aware datetime)
    current_month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    for i in range(36): # 3 years = 36 months
        start_date = current_month_start - relativedelta(months=i)
        end_date = start_date + relativedelta(months=1)
        
        # If processing current month, end_date is now (aware)
        if i == 0:
            end_date = datetime.now(timezone.utc)
            
        await process_month(client, pool, start_date, end_date)
        
        if i < 35: # No need to sleep after the last month
            logger.info("Waiting 10 minutes before next month...")
            await asyncio.sleep(600) # 10 minutes
            
    await client.disconnect()
    await pool.close()
    logger.info("--- ALL HISTORICAL SYNC COMPLETED ---")

if __name__ == "__main__":
    import re # Ensure re is imported for karat parsing
    asyncio.run(main())
