
import asyncio
import os
from datetime import datetime, timedelta
from telethon import TelegramClient
from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_SESSION_NAME,
    TELEGRAM_CHANNEL,
)
from ocr_extractor import extract_prices_from_image, extract_prices_from_text
from telethon.tl.types import MessageMediaPhoto
import tempfile

async def scrape_history(client: TelegramClient, days: int = 30):
    cutoff = datetime.now() - timedelta(days=days)
    results = []
    
    print(f"Fetching history for the last {days} days from {TELEGRAM_CHANNEL}...")
    
    async for message in client.iter_messages(TELEGRAM_CHANNEL):
        if message.date and message.date.replace(tzinfo=None) < cutoff:
            break
            
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
                'date': message.date.strftime("%Y-%m-%d %H:%M"),
                'message_id': message.id,
                'prices': prices,
                'source': 'text' if message.text and extract_prices_from_text(message.text) else 'image',
            })
            print(f"[{results[-1]['date']}] Found: {prices} (Source: {results[-1]['source']})")
    
    return results

async def main():
    client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    
    history = await scrape_history(client, days=30)
    
    print("\n" + "="*30)
    print(f"SCRAPE SUMMARY (Last 30 Days)")
    print("="*30)
    
    if not history:
        print("No prices found.")
    else:
        # Sort by date ascending for the summary
        history.sort(key=lambda x: x['date'])
        for entry in history:
            price_str = " | ".join([f"{k}: {v} DZD" for k, v in entry['prices'].items()])
            print(f"{entry['date']} | {price_str}")
            
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
