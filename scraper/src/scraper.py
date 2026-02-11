"""
Algeria Gold Tracker - Telegram Scraper
Scrapes gold prices from Algerian Telegram channels
"""

import os
import re
import asyncio
import logging
from datetime import datetime
from typing import Optional, Dict, List
from dataclasses import dataclass

from telethon import TelegramClient, events
from telethon.tl.types import Message, MessageMediaPhoto
import asyncpg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Telegram API credentials
API_ID = os.getenv('TELEGRAM_API_ID')
API_HASH = os.getenv('TELEGRAM_API_HASH')
PHONE = os.getenv('TELEGRAM_PHONE')
DATABASE_URL = os.getenv('DATABASE_URL')

# Channels to monitor (add channel usernames here)
# We monitor BijouterieChalabi specifically as requested
CHANNELS = [
    'BijouterieChalabi',
]

@dataclass
class GoldPrice:
    """Represents a gold price data point"""
    timestamp: datetime
    karat: int  # 18, 21, 22, 24
    buy_price: Optional[float]
    sell_price: Optional[float]
    source: str
    raw_text: str
    
    def to_dict(self) -> Dict:
        return {
            'timestamp': self.timestamp.isoformat(),
            'karat': self.karat,
            'buy_price': self.buy_price,
            'sell_price': self.sell_price,
            'source': self.source,
            'raw_text': self.raw_text
        }


class GoldPriceParser:
    """Parses gold prices from Telegram messages"""
    
    # Regex patterns for price extraction
    PATTERNS = {
        # Pattern: "18k: 29600 - 29800 DA" or similar
        'range': re.compile(
            r'(\d{2})[kK]?\s*[:=]?\s*(\d{1,3}[\s,.]?\d{3})\s*[-–]\s*(\d{1,3}[\s,.]?\d{3})\s*(?:DA|دج)?',
            re.IGNORECASE
        ),
        # Pattern: "سعر الـ 18: 29700 دج"
        'single': re.compile(
            r'(?:سعر|prix)?\s*(?:الـ\s*)?(\d{2})\s*[:=]?\s*(\d{1,3}[\s,.]?\d{3})\s*(?:DA|دج)?',
            re.IGNORECASE | re.UNICODE
        ),
        # Pattern: "السبيكة 750" (Sabika/Lingot 18k)
        'sabika': re.compile(
            r'(?:السبيكة|سبيكة|sabika|lingot)\s*(?:750|18[kK])?\s*[:=]?\s*(\d{1,3}[\s,.]?\d{3})\s*(?:DA|دج)?',
            re.IGNORECASE | re.UNICODE
        ),
    }
    
    @classmethod
    def parse_message(cls, message: str, source: str) -> List[GoldPrice]:
        """Extract gold prices from a message"""
        prices = []
        now = datetime.utcnow()
        
        # Try range pattern
        for match in cls.PATTERNS['range'].finditer(message):
            karat = int(match.group(1))
            buy = cls._parse_number(match.group(2))
            sell = cls._parse_number(match.group(3))
            
            if karat in [18, 21, 22, 24]:
                prices.append(GoldPrice(
                    timestamp=now,
                    karat=karat,
                    buy_price=buy,
                    sell_price=sell,
                    source=source,
                    raw_text=match.group(0)
                ))
        
        # Try single price pattern
        for match in cls.PATTERNS['single'].finditer(message):
            karat = int(match.group(1))
            price = cls._parse_number(match.group(2))
            
            if karat in [18, 21, 22, 24]:
                prices.append(GoldPrice(
                    timestamp=now,
                    karat=karat,
                    buy_price=price,
                    sell_price=None,
                    source=source,
                    raw_text=match.group(0)
                ))
        
        # Try sabika pattern (always 18k)
        for match in cls.PATTERNS['sabika'].finditer(message):
            price = cls._parse_number(match.group(1))
            prices.append(GoldPrice(
                timestamp=now,
                karat=18,
                buy_price=price,
                sell_price=None,
                source=source,
                raw_text=match.group(0)
            ))
        
        return prices
    
    @staticmethod
    def _parse_number(text: str) -> float:
        """Parse a number string, handling spaces and commas"""
        cleaned = re.sub(r'[\s,.]', '', text)
        return float(cleaned)


class GoldScraper:
    """Main scraper class for Telegram channels"""
    
    def __init__(self):
        self.client = TelegramClient(
            'gold_scraper_session',
            API_ID,
            API_HASH
        )
        self.parser = GoldPriceParser()
        self.db_pool = None
    
    async def start(self):
        """Start the Telegram client"""
        # Check if using bot token or phone number
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        
        if bot_token:
            logger.info("Starting Telegram client with bot token")
            await self.client.start(bot_token=bot_token)
        else:
            logger.info("Starting Telegram client with phone number")
            await self.client.start(phone=PHONE)
            
        self.db_pool = await asyncpg.create_pool(DATABASE_URL)
        logger.info("Telegram client & DB pool started successfully")
    
    async def stop(self):
        """Stop the Telegram client"""
        await self.client.disconnect()
        if self.db_pool:
            await self.db_pool.close()
        logger.info("Telegram client stopped")
    
    async def save_price(self, price: GoldPrice):
        """Save price to database"""
        if not self.db_pool:
            return
            
        try:
            async with self.db_pool.acquire() as conn:
                await conn.execute("""
                    INSERT INTO gold_prices (timestamp, karat, buy_price, sell_price, source, raw_text, gold_type)
                    VALUES ($1, $2, $3, $4, $5, $6, 'new')
                    ON CONFLICT (timestamp, karat, source) DO NOTHING
                """, price.timestamp, price.karat, price.buy_price, price.sell_price, price.source, price.raw_text)
                logger.info(f"Saved price: {price.karat}k - {price.buy_price} DZD")
        except Exception as e:
            logger.error(f"Error saving price: {e}")

    def setup_handlers(self):
        """Setup event handlers for new messages"""
        @self.client.on(events.NewMessage(chats=CHANNELS))
        async def handler(event):
            if event.message.text:
                logger.info(f"New message from {event.chat.username}")
                prices = self.parser.parse_message(event.message.text, event.chat.username)
                
                if prices:
                    logger.info(f"Found {len(prices)} prices")
                    for price in prices:
                        await self.save_price(price)
                else:
                    logger.info("No prices found in message")


async def main():
    """Main entry point"""
    if not API_ID or not API_HASH:
        logger.error("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH")
        return
    
    scraper = GoldScraper()
    
    try:
        await scraper.start()
        scraper.setup_handlers()
        
        logger.info("Listening for new messages... (Press Ctrl+C to stop)")
        await scraper.client.run_until_disconnected()
    
    finally:
        await scraper.stop()


if __name__ == '__main__':
    asyncio.run(main())