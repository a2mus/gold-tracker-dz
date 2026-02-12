import asyncio
import os
import random
from datetime import datetime, timedelta
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

async def seed_history():
    conn = await asyncpg.connect(DATABASE_URL)
    
    # Base prices
    base_prices = {
        18: 29700,
        21: 34650,
        22: 36300,
        24: 39600
    }
    
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=30)
    
    print(f"Seeding history from {start_date} to {end_date}...")
    
    for i in range(30 * 4):  # 4 points per day
        current_time = start_date + timedelta(hours=i*6)
        
        # Add some random walk variation
        trend = (i / 120) * 500  # Slight upward trend
        noise = random.randint(-200, 200)
        
        for karat, base in base_prices.items():
            price = base - 500 + trend + noise  # Start lower and trend up
            buy_price = round(price, -1)
            sell_price = buy_price + 200
            
            await conn.execute("""
                INSERT INTO gold_prices (timestamp, karat, buy_price, sell_price, source, raw_text, gold_type)
                VALUES ($1, $2, $3, $4, 'seed_data', 'Historical Seed', 'new')
                ON CONFLICT (timestamp, karat, source) DO NOTHING
            """, current_time, karat, buy_price, sell_price)
            
    print("Seeding complete.")
    await conn.close()

if __name__ == '__main__':
    asyncio.run(seed_history())