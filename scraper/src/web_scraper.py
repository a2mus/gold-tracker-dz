import asyncio
import os
import re
import logging
from datetime import datetime
import aiohttp
import asyncpg
from scraper import GoldPriceParser, GoldPrice
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
CHANNEL = 'BijouterieChalabi'
URL = f'https://t.me/s/{CHANNEL}'

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
        logger.info(f"Saved: {price.karat}k - {price.buy_price} at {price.timestamp}")
    except Exception as e:
        logger.error(f"Error saving: {e}")

async def fetch_history():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(URL) as response:
            html = await response.text()
            logger.info(f"Total HTML length: {len(html)} bytes")
            
            # Dump a chunk around message wrap to debug structure
            msg_start = html.find('tgme_widget_message')
            if msg_start != -1:
                logger.info(f"HTML Message Chunk: {html[msg_start:msg_start+1000]}")
            else:
                logger.warning("No 'tgme_widget_message' found in HTML")
                # Check if we are redirected or blocked
                logger.info(f"Full HTML: {html[:2000]}")
            return html

def parse_html(html):
    # Extract message divs
    # <div class="tgme_widget_message_text js-message_text" dir="auto">...</div>
    # <a class="tgme_widget_message_date" href="https://t.me/BijouterieChalabi/1234"><time datetime="2024-01-01T12:00:00+00:00">...</time></a>
    
    # We need to associate text with date. They are usually in the same message container div.
    # Using regex to find blocks might be fragile but let's try to match the structure.
    
    # Simple approach: Split by "tgme_widget_message_wrap"
    messages = html.split('class="tgme_widget_message_wrap"')
    parsed_data = []
    
    parser = GoldPriceParser()
    
    for msg in messages[1:]:  # Skip header
        # Extract text
        text_match = re.search(r'class="tgme_widget_message_text.*?>(.*?)</div>', msg, re.DOTALL)
        if not text_match:
            # Debug: Check why text extraction failed
            if "tgme_widget_message_text" in msg:
                logger.warning(f"Found message div but regex failed. Chunk: {msg[:100]}...")
            continue
        
        raw_html_text = text_match.group(1)
        # Clean HTML tags (br, b, etc)
        clean_text = re.sub(r'<br\s*/>', '\n', raw_html_text)
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        
        logger.info(f"Processing message: {clean_text[:50]}...")
        
        # Extract date
        date_match = re.search(r'datetime="([^"]+)"', msg)
        if not date_match:
            continue
            
        timestamp_str = date_match.group(1)
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except:
            continue
            
        # Parse prices
        prices = parser.parse_message(clean_text, CHANNEL)
        for p in prices:
            p.timestamp = timestamp
            parsed_data.append(p)
            
    return parsed_data

async def main():
    if not DATABASE_URL:
        logger.error("Missing DATABASE_URL")
        return
        
    conn = await get_db_connection()
    try:
        logger.info("Fetching history from web preview...")
        html = await fetch_history()
        prices = parse_html(html)
        
        logger.info(f"Found {len(prices)} prices. Saving...")
        for p in prices:
            await save_price(conn, p)
            
        logger.info("Done.")
    finally:
        await conn.close()

if __name__ == '__main__':
    asyncio.run(main())