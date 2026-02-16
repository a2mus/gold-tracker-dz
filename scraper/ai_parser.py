
import subprocess
import json
import os

SYSTEM_PROMPT = """
You are an expert in the Algerian gold market. Your task is to parse raw text and OCR data from a Telegram channel into structured JSON.

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

OUTPUT FORMAT:
Return ONLY a valid JSON object with these keys:
{
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
"""

def parse_with_ai(raw_text, ocr_text):
    full_prompt = f"{SYSTEM_PROMPT}\n\nParse this Telegram update:\n\nTEXT:\n{raw_text}\n\nOCR:\n{ocr_text}"
    
    try:
        # Call Gemini CLI
        cmd = ["gemini", full_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Extract JSON from response (handling potential markdown blocks)
        raw_output = result.stdout.strip()
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0].strip()
        elif "```" in raw_output:
            raw_output = raw_output.split("```")[1].strip()
            
        return json.loads(raw_output)
    except subprocess.CalledProcessError as e:
        print(f"AI Parsing Error (CalledProcessError): {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None
    except Exception as e:
        print(f"AI Parsing Error: {e}")
        return None

if __name__ == "__main__":
    # Test
    test_text = "سعر السبيكة في سوق الجزائري اليوم 750 يبدأ من 29600دج حتى 29800دج"
    print(json.dumps(parse_with_ai(test_text, ""), indent=2))
