
import asyncio
import os
import json
from datetime import datetime, timedelta
from telethon import TelegramClient
from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_SESSION_NAME,
    TELEGRAM_CHANNEL,
)
from paddleocr import PaddleOCR
from telethon.tl.types import MessageMediaPhoto
import tempfile

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ar')

async def generate_raw_dataset(client: TelegramClient, days: int = 5):
    cutoff = datetime.now() - timedelta(days=days)
    dataset = []
    
    print(f"Generating raw dataset for the last {days} days...")
    
    async for message in client.iter_messages(TELEGRAM_CHANNEL):
        # Convert message date to naive for comparison
        msg_date = message.date.replace(tzinfo=None)
        if msg_date < cutoff:
            break
            
        entry = {
            'date': message.date.isoformat(),
            'message_id': message.id,
            'raw_text': message.text if message.text else "",
            'ocr_text': "",
            'has_media': False
        }
        
        if message.media and isinstance(message.media, MessageMediaPhoto):
            entry['has_media'] = True
            print(f"  Performing OCR on message {message.id}...")
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                await client.download_media(message.media, tmp.name)
                result = ocr.ocr(tmp.name, cls=True)
                if result and result[0]:
                    entry['ocr_text'] = '\n'.join([line[1][0] for line in result[0]])
                os.unlink(tmp.name)
        
        dataset.append(entry)
        print(f"  Processed {message.date.strftime('%Y-%m-%d %H:%M')}")
    
    return dataset

async def main():
    client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    
    raw_data = await generate_raw_dataset(client, days=10)
    
    output_path = '/home/mus/production/gold-tracker-dz/scraper/raw_10day_dataset.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)
        
    print(f"\nDataset saved to {output_path}")
    print(f"Total entries: {len(raw_data)}")
    
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
