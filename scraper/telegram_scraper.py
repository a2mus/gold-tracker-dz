"""
Telegram channel scraper for gold prices.
Connects to @bijouteriechalabi and extracts daily gold prices.
"""
import asyncio
import os
import tempfile
from datetime import datetime, timedelta
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto

from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_SESSION_NAME,
    TELEGRAM_CHANNEL,
)
from ocr_extractor import extract_prices_from_image, extract_prices_from_text


async def get_client() -> TelegramClient:
    """Create and return authenticated Telegram client."""
    client = TelegramClient(
        TELEGRAM_SESSION_NAME,
        TELEGRAM_API_ID,
        TELEGRAM_API_HASH
    )
    await client.start()
    return client


async def scrape_latest_prices(client: TelegramClient, limit: int = 20) -> list[dict]:
    """
    Scrape the latest messages from the gold channel.
    Returns list of {date, prices: {18k, 21k, 22k, 24k}} dicts.
    """
    results = []
    
    async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=limit):
        if not message.date:
            continue
            
        prices = {}
        
        # Try text extraction first
        if message.text:
            prices = extract_prices_from_text(message.text)
        
        # If no prices in text and has image, try OCR
        if not prices and message.media and isinstance(message.media, MessageMediaPhoto):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                await client.download_media(message.media, tmp.name)
                prices = extract_prices_from_image(tmp.name)
                os.unlink(tmp.name)
        
        if prices:
            results.append({
                'date': message.date.isoformat(),
                'message_id': message.id,
                'prices': prices,
                'source': 'text' if message.text else 'image',
            })
    
    return results


async def scrape_history(client: TelegramClient, days: int = 30) -> list[dict]:
    """Scrape historical prices for the past N days."""
    cutoff = datetime.now() - timedelta(days=days)
    results = []
    
    async for message in client.iter_messages(TELEGRAM_CHANNEL):
        if message.date and message.date < cutoff:
            break
            
        prices = {}
        
        if message.text:
            prices = extract_prices_from_text(message.text)
        
        if not prices and message.media and isinstance(message.media, MessageMediaPhoto):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                await client.download_media(message.media, tmp.name)
                prices = extract_prices_from_image(tmp.name)
                os.unlink(tmp.name)
        
        if prices:
            results.append({
                'date': message.date.isoformat(),
                'message_id': message.id,
                'prices': prices,
            })
    
    return results


async def main():
    """Test the scraper."""
    print(f"Connecting to Telegram...")
    client = await get_client()
    
    print(f"Scraping {TELEGRAM_CHANNEL}...")
    prices = await scrape_latest_prices(client, limit=5)
    
    if not prices:
        print("No gold prices found in the latest 5 messages.")
    else:
        for p in prices:
            print(f"[{p['date']}] Source: {p['source']} | Prices: {p['prices']}")
    
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
