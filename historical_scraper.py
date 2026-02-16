import asyncio
import os
import logging
from datetime import datetime, timedelta
import asyncpg
from telethon import TelegramClient
from scraper import GoldPriceParser, GoldPrice
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
CHANNEL_USERNAME = 'BijouterieChalabi'  # Target channel
DAYS_TO_SCRAPE = 30

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)

async def save_price(conn, price: GoldPrice):
    try:
        await conn.execute("""
            INSERT INTO gold_prices (timestamp, karat, buy_price, sell_price, source, raw_text, gold_type)
            VALUES ($1, $2, $3, $4, $5, $6, 'new')
            ON CONFLICT (timestamp, karat, source) DO UPDATE 
            SET buy_price = EXCLUDED.buy_price,
                sell_price = EXCLUDED.sell_price
        """, price.timestamp, price.karat, price.buy_price, price.sell_price, price.source, price.raw_text)
        logger.info(f"Saved price: {price.karat}k - {price.buy_price} DZD at {price.timestamp}")
    except Exception as e:
        logger.error(f"Error saving price: {e}")

async def main():
    # Check if using bot token or phone number
    use_bot = bool(BOT_TOKEN)
    
    if use_bot:
        if not BOT_TOKEN:
            logger.error("Missing TELEGRAM_BOT_TOKEN")
            return
        logger.info("Using bot token for authentication")
    else:
        if not PHONE:
            logger.error("Missing TELEGRAM_PHONE")
            return
        logger.info("Using phone number for authentication")
    
    client = TelegramClient('historical_session', API_ID, API_HASH)
    
    if use_bot:
        await client.start(bot_token=BOT_TOKEN)
    else:
        await client.start(phone=PHONE)
    
    conn = await get_db_connection()
    parser = GoldPriceParser()
    
    try:
        start_date = datetime.utcnow() - timedelta(days=DAYS_TO_SCRAPE)
        logger.info(f"Scraping history from {start_date}...")
        
        count = 0
        async for message in client.iter_messages(CHANNEL_USERNAME, limit=None, offset_date=datetime.utcnow()):
            if message.date.replace(tzinfo=None) < start_date:
                break
            
            if message.text:
                # Use message date as timestamp
                prices = parser.parse_message(message.text, CHANNEL_USERNAME)
                
                for price in prices:
                    # Override timestamp with message timestamp
                    price.timestamp = message.date
                    await save_price(conn, price)
                    count += 1
                    
        logger.info(f"Finished scraping. Total prices saved: {count}")
        
    except Exception as e:
        logger.error(f"Scraping error: {e}")
    finally:
        await client.disconnect()
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())