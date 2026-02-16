
import asyncio
import json
import os
from agents_list import agents_list
from sessions_spawn import sessions_spawn

SYSTEM_PROMPT = """
You are an expert in the Algerian gold market. Your task is to parse a raw dataset of Telegram messages and OCR text into structured JSON.

GOLD MARKET RULES:
1. "يساك" or "كاسي" means used gold (buy-back price).
2. "تكسير" means broken/scrap gold.
3. "750" refers to 18k gold.
4. "999" or "999.9" refers to 24k gold.
5. "سبيكة" means Gold Bar.
6. "لويزة" refers to Gold Coins (Louis).
7. Prices are usually in DZD (دج).
8. Ranges: "يبدأ من X حتى Y" means price_min=X, price_max=Y.
9. Brands like INNOVA, SADE, MONACO are "Imported" (مستورد).

DATASET TO PARSE:
{dataset}

OUTPUT FORMAT:
Return a list of objects, one for each message in the dataset. Each object should have:
{
  "date": "ISO string",
  "message_id": int,
  "market_data": [
    {
      "karat": "18k|21k|22k|24k",
      "gold_type": "Jewelry|Bar|Coin|Scrap",
      "condition": "New|Used|Broken",
      "origin": "Local|Imported|BrandName",
      "price_min": float,
      "price_max": float or null
    }
  ],
  "market_brief": {
    "global_spot_usd": float or null,
    "sentiment": "Bullish|Bearish|Neutral|Correction",
    "ai_summary": "1-sentence summary in English",
    "key_events": ["list of upcoming events"]
  },
  "currency": {
    "usd_buy": float or null,
    "eur_buy": float or null
  },
  "risk_alerts": [
    {"karat": "string", "threshold": float, "description": "string"}
  ]
}

Return ONLY the JSON list.
"""

async def parse_dataset():
    # Read the raw dataset
    with open('/home/mus/production/gold-tracker-dz/scraper/raw_10day_dataset.json', 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    
    # Format prompt
    task = SYSTEM_PROMPT.replace("{dataset}", json.dumps(dataset, ensure_ascii=False, indent=2))
    
    # Spawn sub-agent
    print("Spawning sub-agent for dataset parsing...")
    result = await sessions_spawn(
        task=task,
        label="gold-parsing-expert",
        model="google-antigravity/gemini-3-flash", # Use a reliable model
        thinking="low"
    )
    
    print("Parsing complete.")
    
    # Save the parsed results
    output_path = '/home/mus/production/gold-tracker-dz/scraper/parsed_history.json'
    
    # Extract JSON from sub-agent result
    raw_output = result['announcement']
    if "```json" in raw_output:
        raw_output = raw_output.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_output:
        raw_output = raw_output.split("```")[1].strip()
    
    # Note: Announcement might contain "Run finished: ... result text"
    if "Run finished:" in raw_output:
        raw_output = raw_output.split("Run finished:")[1].strip()

    try:
        parsed_data = json.loads(raw_output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print(f"Parsed data saved to {output_path}")
    except Exception as e:
        print(f"Failed to save parsed data: {e}")
        print(f"Raw output was: {raw_output}")

if __name__ == "__main__":
    asyncio.run(parse_dataset())
