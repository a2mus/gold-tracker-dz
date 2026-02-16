
import asyncio
import os
import json
from datetime import datetime
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import tempfile
from paddleocr import PaddleOCR

# Import from local files
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_SESSION_NAME,
    TELEGRAM_CHANNEL
)

ocr = PaddleOCR(use_angle_cls=True, lang='ar')

async def save_raw_updates(limit=5):
    client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    
    updates = []
    async for message in client.iter_messages(TELEGRAM_CHANNEL, limit=limit):
        ocr_text = ""
        if message.media and isinstance(message.media, MessageMediaPhoto):
            with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                await client.download_media(message.media, tmp.name)
                res = ocr.ocr(tmp.name, cls=True)
                if res and res[0]:
                    ocr_text = '\n'.join([line[1][0] for line in res[0]])
                os.unlink(tmp.name)
        
        updates.append({
            'date': message.date.isoformat(),
            'message_id': message.id,
            'raw_text': message.text or "",
            'ocr_text': ocr_text
        })
    
    output_path = '/home/mus/production/gold-tracker-dz/scraper/latest_raw.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(updates, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(updates)} raw updates to {output_path}")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(save_raw_updates())
