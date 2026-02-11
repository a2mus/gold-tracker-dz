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

from telethon import TelegramClient
from telethon.tl.types import Message, MessageMediaPhoto
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

# Channels to monitor (add channel usernames here)
CHANNELS = [
    # 'channel_username_1',
    # 'channel_username_2',
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
        
        logger.info("Telegram client started successfully")
    
    async def stop(self):
        """Stop the Telegram client"""
        await self.client.disconnect()
        logger.info("Telegram client stopped")
    
    async def scrape_channel(self, channel: str, limit: int = 100) -> List[GoldPrice]:
        """Scrape messages from a channel"""
        prices = []
        
        try:
            async for message in self.client.iter_messages(channel, limit=limit):
                if message.text:
                    parsed = self.parser.parse_message(message.text, channel)
                    prices.extend(parsed)
                    
                    if parsed:
                        logger.info(f"Found {len(parsed)} prices in message {message.id}")
        
        except Exception as e:
            logger.error(f"Error scraping channel {channel}: {e}")
        
        return prices
    
    async def scrape_all(self, limit: int = 50) -> List[GoldPrice]:
        """Scrape all configured channels"""
        all_prices = []
        
        for channel in CHANNELS:
            logger.info(f"Scraping channel: {channel}")
            prices = await self.scrape_channel(channel, limit)
            all_prices.extend(prices)
            
            # Rate limiting
            await asyncio.sleep(2)
        
        return all_prices


async def main():
    """Main entry point"""
    if not API_ID or not API_HASH:
        logger.error("Missing TELEGRAM_API_ID or TELEGRAM_API_HASH")
        logger.info("Get your credentials at https://my.telegram.org/")
        return
    
    scraper = GoldScraper()
    
    try:
        await scraper.start()
        
        # Scrape prices
        prices = await scraper.scrape_all()
        
        logger.info(f"Total prices found: {len(prices)}")
        for price in prices:
            print(price.to_dict())
    
    finally:
        await scraper.stop()


if __name__ == '__main__':
    asyncio.run(main())
